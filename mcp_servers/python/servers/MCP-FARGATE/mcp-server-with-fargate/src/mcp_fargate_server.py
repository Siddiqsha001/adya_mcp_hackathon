import logging
import traceback
from typing import Any, Sequence
import json
from dotenv import load_dotenv
import tools

from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

load_dotenv()

# Tool handler registration
class ToolHandler:
    def __init__(self, name, func, description, arg_schema):
        self.name = name
        self.func = func
        self.description = description
        self.arg_schema = arg_schema

    def get_tool_description(self):
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema=self.arg_schema  # schema shown to model
        )

    def run_tool(self, arguments: dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        try:
            if not isinstance(arguments, dict):
                raise RuntimeError("Tool arguments must be a dictionary.")

            filtered_args = {
                k: v for k, v in arguments.items()
                if "properties" in self.arg_schema and k in self.arg_schema["properties"]
        }


            # Filter out unwanted system-level keys
            # filtered_args = {
            #     k: v for k, v in arguments.items()
            #     if not k.startswith("__") and k != "server_credentials"
            # }

            result = self.func(**filtered_args)

            # Wrap and return as text output
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        except Exception as e:
            logging.error(traceback.format_exc())
            raise RuntimeError(f"Error in tool '{self.name}': {str(e)}")


# Tool registry
tool_handlers = {}

def add_tool_handler(name, func, description, arg_schema):
    tool_handlers[name] = ToolHandler(name, func, description, arg_schema)

def get_tool_handler(name: str) -> ToolHandler | None:
    return tool_handlers.get(name)


# ======================
# Register tools
# ======================
add_tool_handler(
    "create_vpc",
    tools.create_vpc,
    "Create a new VPC. Args: cidr (default 10.0.0.0/16)",
    {"cidr": {"type": "string", "required": False}}
)
add_tool_handler(
    "delete_vpc",
    tools.delete_vpc,
    "Delete a VPC. Args: vpc_id",
    {
        "type": "object",
        "properties": {
            "vpc_id": {
                "type": "string",
                "description": "The ID of the VPC to delete"
            }
        },
        "required": ["vpc_id"]
    }
)

add_tool_handler(
    "list_vpcs",
    tools.list_vpcs,
    "List all VPCs.",
    {}
)
add_tool_handler(
    "create_subnet",
    tools.create_subnet,
    "Create a subnet. Args: vpc_id, cidr, az",
    {
        "type": "object",
        "properties": {
            "vpc_id": {
                "type": "string",
                "description": "The ID of the VPC"
            },
            "cidr": {
                "type": "string",
                "description": "The CIDR block for the subnet"
            },
            "az": {
                "type": "string",
                "description": "The availability zone for the subnet"
            }
        },
        "required": ["vpc_id", "cidr", "az"]
    }
)

add_tool_handler(
    "list_subnets",
    tools.list_subnets,
    "List all subnets.",
    {}
)
add_tool_handler(
    "create_ecs_cluster",
    tools.create_ecs_cluster,
    "Create an ECS cluster. Args: name",
    {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Name of the ECS cluster"
            }
        },
        "required": ["name"]
    }
)

add_tool_handler(
    "list_clusters",
    tools.list_clusters,
    "List all ECS clusters.",
    {}
)

# ======================
# MCP Server Definition
# ======================
app = Server("MCP-FARGATE")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [th.get_tool_description() for th in tool_handlers.values()]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    try:
        if not isinstance(arguments, dict):
            raise RuntimeError("arguments must be dictionary")

        tool_handler = get_tool_handler(name)
        if not tool_handler:
            raise ValueError(f"Unknown tool: {name}")

        return tool_handler.run_tool(arguments)

    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error during call_tool: {str(e)}")
        raise RuntimeError(f"Caught Exception. Error: {str(e)}")


# ======================
# Entry point
# ======================
async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
