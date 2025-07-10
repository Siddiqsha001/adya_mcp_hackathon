import os
import httpx
from typing import Dict, Any, List
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load env variables from .env
load_dotenv()

PORTAINER_API = os.getenv("PORTAINER_API")  # Example: https://localhost:9443/api
USERNAME = os.getenv("PORTAINER_USERNAME")
PASSWORD = os.getenv("PORTAINER_PASSWORD")

# Create MCP server instance
server = FastMCP("MCP-PORTAINER")

# Get Portainer JWT token
async def get_token() -> str:
    print(f"Authenticating to {PORTAINER_API} as {USERNAME}")
    async with httpx.AsyncClient(verify=False) as client:
        res = await client.post(
            f"{PORTAINER_API}/auth",
            json={"Username": USERNAME, "Password": PASSWORD}
        )
    res.raise_for_status()
    return res.json().get("jwt")

# Get endpoint ID from Portainer
async def get_endpoint_id(token: str) -> int:
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(verify=False) as client:
        res = await client.get(f"{PORTAINER_API}/endpoints", headers=headers)
    res.raise_for_status()
    data = res.json()
    if not data:
        raise ValueError(" No environments (endpoints) found in Portainer.")
    return data[0]["Id"]  # Or filter by name if needed

# Tool: List containers
@server.tool(name="list_portainer_containers")
async def list_portainer_containers() -> List[Dict[str, Any]]:
    """
    List all Docker containers managed by Portainer.
    """
    token = await get_token()
    endpoint_id = await get_endpoint_id(token)
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(verify=False) as client:
        res = await client.get(
            f"{PORTAINER_API}/endpoints/{endpoint_id}/docker/containers/json",
            headers=headers
        )
    res.raise_for_status()
    return res.json()

# Tool: Start container
@server.tool()
async def start_container(container_id: str) -> str:
    """
    Start a Docker container using its container ID.
    """
    token = await get_token()
    endpoint_id = await get_endpoint_id(token)
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(verify=False) as client:
        res = await client.post(
            f"{PORTAINER_API}/endpoints/{endpoint_id}/docker/containers/{container_id}/start",
            headers=headers
        )
    if res.status_code == 204:
        return f"Container {container_id} started successfully."
    return f"Failed to start container {container_id}: {res.text}"

# Tool: Stop container
@server.tool()
async def stop_container(container_id: str) -> str:
    """
    Stop a Docker container using its container ID.
    """
    token = await get_token()
    endpoint_id = await get_endpoint_id(token)
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(verify=False) as client:
        res = await client.post(
            f"{PORTAINER_API}/endpoints/{endpoint_id}/docker/containers/{container_id}/stop",
            headers=headers
        )
    if res.status_code == 204:
        return f"Container {container_id} stopped successfully."
    return f"Failed to stop container {container_id}: {res.text}"

# Tool: Get container logs
@server.tool()
async def get_container_logs(container_id: str) -> str:
    """
    Get logs of a Docker container using its container ID.
    """
    token = await get_token()
    endpoint_id = await get_endpoint_id(token)
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(verify=False) as client:
        res = await client.get(
            f"{PORTAINER_API}/endpoints/{endpoint_id}/docker/containers/{container_id}/logs?stdout=true&stderr=true&tail=100",
            headers=headers
        )
    if res.status_code == 200:
        return res.text
    return f"Failed to get logs for container {container_id}: {res.text}"

# Run the server using stdio transport
if __name__ == "__main__":
    server.run(transport="stdio")
