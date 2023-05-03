from pulumi import ComponentResource, Output, ResourceOptions, Config
import pulumi_aws as aws


class WebServiceArgs:
  def __init__(self,
    env="development",
    db_host=None,
    db_port=None,
    db_name=None,
    db_user=None,
    db_password=None,
    vpc_id=None,
    image_name=None,
    role_arn=None,
    cluster_arn=None,
    task_cpu="256",
    task_mem="512",
    desired_capacity="1",
    subnet_ids=None,  # array of subnet IDs
    security_group_ids=None # array of security group Ids
  ):
    self.env = env
    self.db_host = db_host
    self.db_port = db_port
    self.db_name = db_name
    self.db_user = db_user
    self.db_password = db_password
    self.vpc_id = vpc_id
    self.image_name = image_name
    self.role_arn = role_arn
    self.cluster_arn = cluster_arn
    self.task_cpu = task_cpu
    self.task_mem = task_mem
    self.desired_capacity = desired_capacity
    self.subnet_ids = subnet_ids
    self.security_group_ids = security_group_ids

class WebService(ComponentResource):
  def __init__(self,
    name: str,
    args: WebServiceArgs,
    opts: ResourceOptions = None
  ):
    super().__init__("custom:resource:Frontend", name, {}, opts)

    # Create a load balancer to listen for HTTP traffic on port 80
    self.alb = aws.lb.LoadBalancer(f"{name}-app-lb",
      security_groups=args.security_group_ids,
      subnets=args.subnet_ids,
      opts=ResourceOptions(parent=self)
    )

    # Create a target group to adopt the service on 80 port
    app_tg = aws.lb.TargetGroup(f"{name}-app-tg",
      port=80,
      protocol="HTTP",
      target_type="ip",
      vpc_id=args.vpc_id,
      health_check=aws.lb.TargetGroupHealthCheckArgs(
        healthy_threshold=5,
        interval=300,
        timeout=60,
        protocol="HTTP",
        matcher="200-399"
      ),
      opts=ResourceOptions(parent=self)
    )

    # Create a load balancer listener
    alb_listener = aws.lb.Listener(f"{name}-app-listener",
      load_balancer_arn=self.alb.arn,
      port=80,
      default_actions=[aws.lb.ListenerDefaultActionArgs(
        type="forward",
        target_group_arn=app_tg.arn,
      )],
      opts=ResourceOptions(parent=self)
    )

    # Spin up a load balanced service running our container image.
    task_name = f"{name}-app-task"
    container_name = f"{name}-app"
    self.task_definition=aws.ecs.TaskDefinition(task_name,
      family="fargate-task-definition",
      cpu=args.task_cpu,
      memory=args.task_mem,
      network_mode="awsvpc",
      requires_compatibilities=[
        "FARGATE"],
      execution_role_arn=args.role_arn,
      task_role_arn=args.role_arn,
      container_definitions=Output.json_dumps([{
        "name": container_name,
        "image": args.image_name,
        "portMappings": [{
          "containerPort": 80,
          "hostPort": 80,
          "protocol": "tcp"
        }],
        "environment": [
          {
            "name": "DB_HOST",
            "value": args.db_host
          },
          {
            "name": "DB_PORT",
            "value": args.db_port
          },
          {
            "name": "DB_NAME",
            "value": args.db_name
          },
          {
            "name": "DB_USER",
            "value": args.db_user
          },
          {
            "name": "DB_PASSWORD",
            "value": args.db_password
          },
          {
            "name": "LB_HOSTNAME",
            "value": self.alb.dns_name
          },
          {
            "name": "RAILS_ENV",
            "value": args.env
          },
        ]
      }]),
      opts=ResourceOptions(parent=self)
    )

    self.service = aws.ecs.Service(f"{name}-app-svc",
      cluster=args.cluster_arn,
      desired_count=args.desired_capacity,
      launch_type="FARGATE",
      task_definition=self.task_definition.arn,
      enable_execute_command = True,
      network_configuration=aws.ecs.ServiceNetworkConfigurationArgs(
        assign_public_ip=True,
        subnets=args.subnet_ids,
        security_groups=args.security_group_ids
      ),
      load_balancers=[aws.ecs.ServiceLoadBalancerArgs(
        target_group_arn=app_tg.arn,
        container_name=container_name,
        container_port=80,
      )],
      opts=ResourceOptions(
        depends_on=[alb_listener], parent=self),
      )

    self.register_outputs({})
