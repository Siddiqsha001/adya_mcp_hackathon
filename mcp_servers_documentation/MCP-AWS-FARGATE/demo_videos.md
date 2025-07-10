# AWS Fargate MCP Server – Demos and Payload Examples

## 🎥 Demo Video
- **MCP server setup explanation + API Gathering + Features Testing**: https://drive.google.com/drive/folders/1V4SD_cCecPHiw3ys_71bo0KyR-dHQWw0

---

## 🔐 Credential JSON Payload
Example payload format for sending credentials to the MCP Server:
```json
{
  "AWS_FARGATE": {
    "AWS_ACCESS_KEY_ID": "AKIAIOSFODNN7EXAMPLE",
    "AWS_SECRET_ACCESS_KEY": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "AWS_REGION": "us-west-2"
  }
}
```

## 📋 Example Tool Calls

### Create VPC
```python
response = await session.execute("create_vpc", {"cidr_block": "10.0.0.0/16", "name": "my-mcp-vpc"})
print(response)
```

### List VPCs
```python
response = await session.execute("list_vpcs")
print(response)
```

### Create ECS Cluster
```python
response = await session.execute("create_ecs_cluster", {"cluster_name": "my-mcp-cluster"})
print(response)
```

### Create Subnet
```python
response = await session.execute("create_subnet", {
    "vpc_id": "vpc-1234567890abcdef0", 
    "cidr_block": "10.0.1.0/24", 
    "availability_zone": "us-west-2a"
})
print(response)
```
