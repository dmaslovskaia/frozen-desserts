from pulumi import Config, Output, export, StackReference
# import pulumi_docker as docker
import deploy
import build

config = Config()

service_name = config.get("service_name")

stack_ref = StackReference(config.get("manual_stack"))

### 1 STEP: Prepare new docker image for service ###
# application_image = build.Build(service_name, build.BuildArgs())

### 2 STEP: Test container before deploy ###
#app_container = docker.Container(f"{service_name}-test1", 
#  image=application_image.app_image.base_image_name, 
#  envs=["RAILS_ENV=test", "LB_HOSTNAME=127.0.0.1"],
#)

### 3 STEP: Deploy new version of service
front=deploy.WebService(f"{service_name}", 
  deploy.WebServiceArgs(
    env=config.get("environment"),
    db_host=stack_ref.get_output("rds_db_host"),
    db_port=stack_ref.get_output("rds_db_port"),
    db_name=stack_ref.get_output("rds_db_name"),
    db_user=stack_ref.get_output("rds_db_user"),
    db_password=stack_ref.get_output("rds_db_password"),
    vpc_id=stack_ref.get_output("vpc_id"),
    role_arn=stack_ref.get_output("ecs_iam_role_arn"),
    cluster_arn=stack_ref.get_output("ecs_cluster_arn"),
    image_name=config.get("image_name"), # application_image.app_image.base_image_name,
    subnet_ids=stack_ref.get_output("subnet_ids"),
    security_group_ids=stack_ref.get_output("security_group_ids"),
))

web_url=Output.concat("http://", front.alb.dns_name)
export("Web Service URL", web_url)