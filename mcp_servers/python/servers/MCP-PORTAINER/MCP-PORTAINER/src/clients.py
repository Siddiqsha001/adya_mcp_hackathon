import os
from dotenv import load_dotenv
load_dotenv()

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Load your Gemini API Key
gemini_api_key = os.getenv("GOOGLE_API_KEY")
if not gemini_api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env")

# ✅ Load Gemini model
model = ChatGoogleGenerativeAI(
    google_api_key=gemini_api_key,
    model="gemini-1.5-pro-latest"
)

# ✅ Path to server.py (your MCP-PORTAINER)
server_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../servers/MCP-PORTAINER/src/server.py")

server_params = StdioServerParameters(
    command="python",
    args=[server_py],
)

# ✅ Custom prompt for Portainer agent
AGENT_PROMPT = """
You are a helpful assistant with access to Docker containers via Portainer.

You can use the following tools:

1. list_portainer_containers() -> List all Docker containers.
2. start_container(container_id: str) -> Start a specific container.
3. stop_container(container_id: str) -> Stop a specific container.
4. get_container_logs(container_id: str) -> Get logs of a container.

When responding, use the tools as needed.
Always present your final answer in the following format:

Answer:
<your answer here>

Data Used:
- <summarize tool calls/results used>
"""


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Connected to Portainer MCP Server!")
            tools = await load_mcp_tools(session)

            agent = create_react_agent(
                model,
                tools,
                prompt=AGENT_PROMPT,
            )

            # ✅ 🔁 Update your prompt below to test different tool calls
            prompt = "List all Docker containers running in Portainer"

            print(f"\n🔍 Prompt: {prompt}")
            response = await agent.ainvoke({"messages": prompt})

            print("\n✅ Agent Response:\n")
            print(response)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
