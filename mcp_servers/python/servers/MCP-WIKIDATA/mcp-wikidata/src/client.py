
import os
from dotenv import load_dotenv
load_dotenv()

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
# from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Use Gemini from langchain_google_genai
from langchain_google_genai import ChatGoogleGenerativeAI
# You need a Gemini API key for Google Generative AI
gemini_api_key = os.getenv("GOOGLE_API_KEY")
if not gemini_api_key:
    raise ValueError("GOOGLE_API_KEY not found. Please add it to your .env file.")


# os.environ["OPENAI_API_KEY"] = "your-api-key"

model = ChatGoogleGenerativeAI(
    google_api_key=gemini_api_key,
    model="gemini-2.5-pro"
)


server_py = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")
server_params = StdioServerParameters(
    command="python",
    args=[server_py],
)

AGENT_PROMPT = """
You are a helpful assistant with access to the following tools for interacting with Wikidata:

1. search_entity(query: str) -> str
   - Find the Wikidata entity ID for a given concept or name.

2. search_property(query: str) -> str
   - Find the Wikidata property ID for a given property name.

3. get_properties(entity_id: str) -> List[str]
   - List all property IDs associated with a Wikidata entity.

4. execute_sparql(sparql_query: str) -> str
   - Run a SPARQL query on Wikidata for advanced data retrieval.

5. get_metadata(entity_id: str, language: str = "en") -> Dict[str, str]
   - Get the label and description for a Wikidata entity in the specified language.

When answering, use the tools as needed to find accurate information. 
*Always present your final answer in the following format:*

Answer:
<your answer here>

Data Used:
- <summarize the tool calls and results you used, e.g., entity IDs, property IDs, SPARQL results, etc.>
"""



async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(
                model,
                tools,
                prompt=AGENT_PROMPT,
            )
            agent_response = await agent.ainvoke(
                {
                    "messages": "Can you recommend me a movie directed by Bong Joonho?",
                }
            )
            print(agent_response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
