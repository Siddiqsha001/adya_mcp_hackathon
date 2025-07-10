import boto3
import botocore.exceptions


# ======================
# VPC TOOLS
# ======================

def create_vpc(cidr: str = "10.0.0.0/16"):
    ec2 = boto3.client("ec2")
    try:
        vpc = ec2.create_vpc(CidrBlock=cidr)
        return {
            "VpcId": vpc["Vpc"]["VpcId"],
            "State": vpc["Vpc"]["State"]
        }
    except botocore.exceptions.ClientError as e:
        return {"error": str(e)}


def delete_vpc(vpc_id: str):
    ec2 = boto3.client("ec2")
    try:
        ec2.delete_vpc(VpcId=vpc_id)
        return {"message": f"Deleted VPC {vpc_id}"}
    except botocore.exceptions.ClientError as e:
        return {"error": str(e)}


def list_vpcs():
    ec2 = boto3.client("ec2")
    vpcs = ec2.describe_vpcs()
    return {
        "Vpcs": [
            {"VpcId": v["VpcId"], "CidrBlock": v["CidrBlock"], "State": v["State"]}
            for v in vpcs["Vpcs"]
        ]
    }


# ======================
# SUBNET TOOLS
# ======================

def create_subnet(vpc_id: str, cidr: str, az: str):
    ec2 = boto3.client("ec2")
    try:
        subnet = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr,
            AvailabilityZone=az
        )
        return {
            "SubnetId": subnet["Subnet"]["SubnetId"],
            "State": subnet["Subnet"]["State"]
        }
    except botocore.exceptions.ClientError as e:
        return {"error": str(e)}


def list_subnets():
    ec2 = boto3.client("ec2")
    subnets = ec2.describe_subnets()
    return {
        "Subnets": [
            {
                "SubnetId": s["SubnetId"],
                "CidrBlock": s["CidrBlock"],
                "VpcId": s["VpcId"],
                "AvailabilityZone": s["AvailabilityZone"]
            }
            for s in subnets["Subnets"]
        ]
    }


# ======================
# ECS TOOLS
# ======================

# def create_ecs_cluster(name: str):
#     ecs = boto3.client("ecs")
#     try:
#         response = ecs.create_cluster(clusterName=name)
#         return {"ClusterArn": response["cluster"]["clusterArn"]}
#     except botocore.exceptions.ClientError as e:
#         return {"error": str(e)}

def create_ecs_cluster(name: str):
    ecs = boto3.client("ecs")
    try:
        response = ecs.create_cluster(
            clusterName=name,
            capacityProviders=["FARGATE", "FARGATE_SPOT"]
        )
        return {"ClusterArn": response["cluster"]["clusterArn"]}
    except botocore.exceptions.ClientError as e:
        return {"error": str(e)}

def list_clusters():
    ecs = boto3.client("ecs")
    try:
        clusters = ecs.list_clusters()
        return {"Clusters": clusters["clusterArns"]}
    except botocore.exceptions.ClientError as e:
        return {"error": str(e)}


