# AWS Fargate MCP Server Credentials

## Overview
This document provides instructions on obtaining and structuring the credentials needed to connect the AWS Fargate MCP Server in the Vanij Platform.

---

## Credential Format
```json
{
  "AWS_FARGATE": {
    "AWS_ACCESS_KEY_ID": "your-aws-access-key-id",
    "AWS_SECRET_ACCESS_KEY": "your-aws-secret-access-key",
    "AWS_REGION": "your-aws-region"
  }
}
```

## How to Obtain Credentials

1. **AWS IAM Console**: Create an IAM user with programmatic access
   - Log in to your AWS account and navigate to IAM service
   - Create a new user or select an existing one
   - Attach policies that grant permissions for:
     - AWS Fargate
     - Amazon ECS
     - EC2 (for VPC management)
     - CloudWatch (for logs)

2. **Required Permissions**: The IAM user needs these permissions:
   - `AmazonECS-FullAccess`
   - `AmazonEC2ContainerRegistryFullAccess`
   - `CloudWatchLogsFullAccess`
   - Custom policy for VPC management

3. **Security Best Practices**:
   - Use IAM roles for production deployments instead of access keys
   - Implement least privilege principle - only grant necessary permissions
   - Regularly rotate access keys
   - Consider using AWS Secrets Manager for credential storage
