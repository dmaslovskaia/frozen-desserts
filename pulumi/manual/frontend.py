from pulumi import ComponentResource, Output, ResourceOptions
import pulumi_aws as aws
import json


class ECSCluster(ComponentResource):
  def __init__(self,
    name: str,
    opts: ResourceOptions = None
  ):
    super().__init__("custom:resource:ECS", name, opts)

    # Create an ECS cluster to run a container-based service.
    self.cluster = aws.ecs.Cluster(f"{name}-ecs",
      opts=ResourceOptions(parent=self)
    )

    # Create an IAM role that can be used by service"s task
    self.ecs_task_manager_role = aws.iam.Role(f"{name}-task-role",
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

    rpa = aws.iam.RolePolicyAttachment(f"{name}-task-policy",
      role=self.ecs_task_manager_role.name,
      policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
      opts=ResourceOptions(parent=self)
    )

    self.register_outputs({})
