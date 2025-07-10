ClientsConfig =[
    "MCP_CLIENT_AZURE_AI",
    "MCP_CLIENT_OPENAI",
	"MCP_CLIENT_GEMINI"
]
ServersConfig = [
	{
		"server_name": "MCP-GSUITE",
		"command":"uv",
		"args": [
			"--directory",
			"../servers/MCP-GSUITE/mcp-gsuite",
			"run",
			"mcp-gsuite"
		]
	},
    {
		"server_name": "abstractapi-mcp-server",
		"command":"uv",
		"args": [
			"--directory",
			"../servers/abstractapi-mcp-server",
			"run",
			"server.py"
		]
	},
    {
		"server_name": "MCP-PINECONE-DEV",
		"command":"uv",
		"args": [
			"--directory",
			"../servers/MCP-PINECONE",
			"run",
			"mcp-pinecone"
		]
	},
    {
		"server_name": "MCP-PINECONE-PUBLISHED",
		"command":"uvx",
		"args": [
			"mcp-pinecone",
			"--index-name",
			"q-and-a-system",
			"--api-key",
			"pcsk_4wxP35_Paz2m6Fjgg4u1sBpeEC45LABjQhKykMNRqAtbzxEc4XRpnRRFSHZ3BeM9Pvf91D"
		]
	}
]
