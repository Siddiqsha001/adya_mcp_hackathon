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
			"../servers/abstractapi-mcp-server/mcp-gsuite",
			"run",
			"mcp-gsuite"
		]
	}
]