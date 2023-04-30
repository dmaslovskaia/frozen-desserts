"""An AWS Python Pulumi program"""

from pulumi import Config, Output, export
import pulumi_aws as aws
import pulumi_docker as docker
import pulumi_random as random
import network
import backend
import frontend


config = Config()

service_name = config.get("service_name") or "frozen-desserts"
db_name=config.get("db_name")
db_user=config.get("db_user")
db_port=config.get("db_port")

# Get secretified password from config and protect it going forward, or create one using the "random" provider.
db_password=config.get_secret("db_password")
if not db_password:
  password=random.RandomPassword("db_password",
    length=16,
    special=True,
    override_special="_%@",
  )
  # Pulumi knows this provider is used to create a password and thus automatically protects it going forward.
  db_password=password.result

### 1 STEP ###
# Create a private ECR repository.
ecr_repo = aws.ecr.Repository("ecr-repository", name="frozen-desserts")
# Get authorisation token to push image to ECR
auth_token = aws.ecr.get_authorization_token_output(registry_id=ecr_repo.registry_id)
# Build and push image
app_image = docker.Image("frodes",
    build=docker.DockerBuildArgs(
      context="../",
      dockerfile="./app/Dockerfile",
    ),
    image_name=ecr_repo.repository_url.apply(lambda repository_url: f"{repository_url}:latest"),
    registry=docker.RegistryArgs(
      username="AWS",
      password=Output.secret(auth_token.password),
      server=ecr_repo.repository_url,
    ),
    skip_push=False)
export("imageName", app_image.image_name)

# Attaching an application life cycle policy to the storage
app_lifecycle_policy = aws.ecr.LifecyclePolicy("app-lifecycle-policy",
  repository=ecr_repo.name,
  policy="""{
    "rules": [
      {
        "rulePriority": 10,
        "description": "Remove untagged images",
        "selection": {
          "tagStatus": "untagged",
          "countType": "imageCountMoreThan",
          "countNumber": 0
        },
        "action": {
          "type": "expire"
        }
      }
    ]
  }"""
)

### 2 STEP ###

# Create an AWS VPC and subnets, etc
network=network.Vpc(f"{service_name}-net", network.VpcArgs())
subnet_ids=[]
for subnet in network.subnets:
  subnet_ids.append(subnet.id)

# Create a backend DB instance
back=backend.Db(f"{service_name}-db", backend.DbArgs(
    db_name=db_name,
    db_user=db_user,
    db_password=db_password,
    # publicly_accessible=True,  # Uncomment this to override for testing
    subnet_ids=subnet_ids,
    security_group_ids=[network.rds_security_group.id]
))

front=frontend.WebService(f"{service_name}-app", frontend.WebServiceArgs(
    db_host=back.db.address,
    db_port=db_port,
    db_name=back.db.name,
    db_user=back.db.username,
    db_password=back.db.password,
    vpc_id=network.vpc.id,
    image_name=app_image.image_name,
    subnet_ids=subnet_ids,
    security_group_ids=[network.fe_security_group.id]
))

web_url=Output.concat("http://", front.alb.dns_name)
export("Web Service URL", web_url)
export("ECS Cluster Name", front.cluster.name)

export("DB Endpoint", back.db.address)
export("DB User Name", back.db.username)
export("DB Password", back.db.password)
