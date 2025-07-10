from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_mcp import FastApiMCP

import tools  # your tools.py

import os
import json

from dotenv import load_dotenv  # <-- Add this import

load_dotenv()  # <-- Load environment variables from .env

# Load client/server configuration
def load_client_configs():
    config_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "clients")
    server_client_config_path = os.path.join(config_dir, "server_client_config.json")
    client_server_execution_path = os.path.join(config_dir, "client_server_execution.json")
    configs = {}
    if os.path.exists(server_client_config_path):
        with open(server_client_config_path, "r") as f:
            configs["server_client_config"] = json.load(f)
    if os.path.exists(client_server_execution_path):
        with open(client_server_execution_path, "r") as f:
            configs["client_server_execution"] = json.load(f)
    return configs

client_configs = load_client_configs()

# Create FastAPI app
app = FastAPI(
    title="Infrastructure Agent API",
    description="Dynamically creates AWS resources through callable tools",
    version="1.0.0"
)

# Define available tools and their mappings to functions in tools.py
tool_map = {
    "create_vpc": tools.create_vpc,
    "delete_vpc": tools.delete_vpc,
    "list_vpcs": tools.list_vpcs,
    "create_subnet": tools.create_subnet,
    "list_subnets": tools.list_subnets,
    "create_ecs_cluster": tools.create_ecs_cluster,
    "list_clusters": tools.list_clusters,
}

# POST endpoint that takes action name and optional parameters
@app.post("/tool", operation_id="trigger_tool")
async def tool_runner(request: Request):
    try:
        body = await request.json()
        action = body.get("action")
        params = body.get("params", {})
        client_id = body.get("client_id")

        if not action:
            return JSONResponse(
                status_code=400,
                content={"error": "Missing 'action' in request body"}
            )

        # Optionally, use client_id to load specific config
        if client_id and client_id in client_configs.get("server_client_config", {}):
            client_config = client_configs["server_client_config"][client_id]
            params.update(client_config)  # Merge client config into params

        func = tool_map.get(action)
        if not func:
            return JSONResponse(
                status_code=404,
                content={"error": f"Tool '{action}' not found"}
            )

        result = func(**params)
        return {"result": result}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Internal server error: {str(e)}"}
        )

@app.get("/")
def health():
    return {"message": "FastAPI MCP AWS Infra Tool Server is running"}

# Register MCP wrapper for agent discovery
mcp = FastApiMCP(
    app,
    name="Infra Tool MCP",
    description="Exposes AWS resource tools to LLM agents",
    include_operations=["trigger_tool"]
)

# Dynamically register MCP-FARGATE for each client (if needed)
# This is a placeholder for more advanced registration logic
for client_id in client_configs.get("server_client_config", {}):
    # You can extend this to register per-client tools if needed
    pass

# Mount the MCP routes
mcp.mount(app)
