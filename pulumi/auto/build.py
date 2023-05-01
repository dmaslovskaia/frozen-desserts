from pulumi import ComponentResource, ResourceOptions, Output
from pulumi_aws import ecr
import pulumi_docker as docker


class BuildArgs:
  def __init__(self,
    context_path="../..",
    dockerfile_path="../../Dockerfile",
  ):
    self.context_path = context_path
    self.dockerfile_path = dockerfile_path

class Build(ComponentResource):
  def __init__(self,
    name: str,
    args: BuildArgs,
    opts: ResourceOptions = None
  ):
    super().__init__("custom:resource:DOCKER", name, {}, opts)

    # Create a private ECR repository.
    ecr_repo = ecr.Repository(f"{name}-ecr", name=name)

    # Get authorisation token to push image to ECR
    auth_token = ecr.get_authorization_token_output(registry_id=ecr_repo.registry_id)

    # Build and push image
    self.app_image = docker.Image(f"{name}-app",
      build=docker.DockerBuildArgs(
        context=args.context_path,
        dockerfile=args.dockerfile_path,
      ),
      image_name=ecr_repo.repository_url.apply(lambda repository_url: f"{repository_url}:latest"),
      registry=docker.RegistryArgs(
        username="AWS",
        password=Output.secret(auth_token.password),
        server=ecr_repo.repository_url,
      ),
    )

    # Attach an application life cycle policy to the storage
    app_lifecycle_policy = ecr.LifecyclePolicy(f"{name}-app-lc-policy",
      repository=ecr_repo.name,
      policy="""{
        "rules": [
          {
            "rulePriority": 10,
            "description": "Remove untagged images",
            "selection": {
              "tagStatus": "untagged",
              "countType": "imageCountMoreThan",
              "countNumber": 1
            },
            "action": {
              "type": "expire"
            }
          }
        ]
      }"""
    )
    self.register_outputs({})
