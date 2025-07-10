# Portainer MCP Server Credentials

## Overview
This document provides instructions on obtaining and structuring the credentials needed to connect the Portainer MCP Server in the Vanij Platform.

---

## Credential Format
```json
{
  "PORTAINER": {
    "PORTAINER_API": "https://your-portainer-instance-url/api",
    "PORTAINER_USERNAME": "your-portainer-username",
    "PORTAINER_PASSWORD": "your-portainer-password"
  }
}
```

## How to Obtain Credentials

1. **Portainer URL**: Use the URL of your Portainer instance followed by `/api` (e.g., `https://portainer.yourdomain.com/api`)

2. **Username & Password**: Use the credentials you created when setting up your Portainer instance
   - If you're using an organization's Portainer, contact your system administrator for API access
   - Ensure your user account has sufficient permissions to manage containers

3. **Security Notes**:
   - Store credentials securely using environment variables
   - Avoid hardcoding credentials in your application
   - Consider using API tokens instead of username/password for production environments
