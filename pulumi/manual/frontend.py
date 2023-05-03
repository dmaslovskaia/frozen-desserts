from pulumi import ComponentResource, Output, ResourceOptions
from pulumi_aws import ecr, ecs, iam
import json


class ECSCluster(ComponentResource):
  def __init__(self,
    name: str,
    opts: ResourceOptions = None
  ):
    super().__init__("custom:resource:ECS", name, opts)

    # Create a private ECR repository.
    ecr_repo = ecr.Repository(f"{name}-ecr", name=name)

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

    # Create an ECS cluster to run a container-based service.
    self.cluster = ecs.Cluster(f"{name}-ecs",
      opts=ResourceOptions(parent=self)
    )

    # Create an IAM role that can be used by service"s task
    self.ecs_task_manager_role = iam.Role(f"{name}-task-role",
      assume_role_policy=json.dumps({
        "Version": "2008-10-17",
        "Statement": [{
          "Sid": "",
          "Effect": "Allow",
          "Principal": {
            "Service": "ecs-tasks.amazonaws.com"
          },
          "Action": "sts:AssumeRole",
        }]
      }),
      opts=ResourceOptions(parent=self)
    )

    rpa = iam.RolePolicyAttachment(f"{name}-task-policy",
      role=self.ecs_task_manager_role.name,
      policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
      opts=ResourceOptions(parent=self)
    )

    self.register_outputs({})
