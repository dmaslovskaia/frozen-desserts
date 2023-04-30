"""An AWS Python Pulumi program"""

from pulumi import Config, Output, export
import pulumi_aws as aws
import pulumi_docker as docker


config = Config()

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
