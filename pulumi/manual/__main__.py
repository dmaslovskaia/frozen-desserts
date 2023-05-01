from pulumi import Config, export
import frontend
import network
import backend

config = Config()

service_name = config.get("service_name")

# Create an AWS VPC resources
network_core=network.Vpc(service_name, 
  network.VpcArgs(cidr_block=config.get("vpc_cidr_block")), 
  network.ExtArgs(rds_db_port=config.get("db_port"))
)
subnet_ids=[]
for subnet in network_core.subnets:
  subnet_ids.append(subnet.id)

# Create a backend RDS instance resources
back=backend.Db(service_name, backend.DbArgs(
    db_name=config.get("db_name"),
    db_user=config.get_secret("db_user"),
    db_password=config.get_secret("db_password"),
    subnet_ids=subnet_ids,
    security_group_ids=[network_core.rds_security_group.id]
))

# Prepare a ECS Cluster
ecs_cluster=frontend.ECSCluster(service_name)

export("ecs_cluster_arn", ecs_cluster.cluster.arn)
export("rds_db_host", back.db.address)
export("rds_db_port", config.get("db_port"))
export("rds_db_name", back.db.name)
export("rds_db_user", back.db.username)
export("rds_db_password", back.db.password)
export("vpc_id", network_core.vpc.id)
export("subnet_ids", subnet_ids)
export("security_group_ids", [network_core.fe_security_group.id])
export("ecs_iam_role_arn", ecs_cluster.ecs_task_manager_role.arn)
