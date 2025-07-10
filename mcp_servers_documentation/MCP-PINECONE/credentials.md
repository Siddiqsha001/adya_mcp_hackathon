# Pinecone MCP Server - Credentials Setup

<div align="center">
    <img src="https://pinecone.io/images/pinecone_logo_dark.svg" width="300" alt="Pinecone Logo">
    <h2>Configuring Authentication for Pinecone MCP Server</h2>
</div>

---

## 🔑 API Key Requirements

To use the Pinecone MCP Server, you need a Pinecone account and API key. This allows you to access and manage your vector indexes.

---

## 📝 How to Get a Pinecone API Key

1. **Create a Pinecone Account**: Visit [Pinecone](https://www.pinecone.io/) and sign up
2. **Create a Project**: Set up a new project in the Pinecone console
3. **Create an Index**: Set up a vector index with appropriate dimensions (typically 768, 1024, or 1536 depending on your embedding model)
4. **Get Your API Key**: From your Pinecone console, navigate to API Keys and create or copy your key

---

## ⚙️ Server Configuration

The Pinecone MCP Server can be configured in two ways:

### Option 1: Command Line Arguments

When starting the server, provide your API key and index name:

```bash
uvx mcp-pinecone --index-name your_index_name --api-key your_api_key
```

### Option 2: Environment Variables

Create a `.env` file in the Pinecone MCP server directory with:

```
PINECONE_API_KEY=your_api_key_here
PINECONE_INDEX_NAME=your_index_name
```

---

## 🔍 Pinecone Index Configuration

For optimal performance, configure your Pinecone index with:

- **Dimensions**: Match your embedding model (e.g., 1536 for OpenAI embeddings)
- **Metric**: cosine (recommended for most semantic search cases)
- **Environment**: Choose based on your region and latency requirements
- **Pods**: Select based on your data volume and query performance needs

---

## 📊 Understanding Pinecone Resources

- **Index**: The main container for your vector data
- **Namespace**: Logical separation within an index (optional)
- **Vector Dimensions**: Must match your embedding model
- **Metadata**: Additional information stored alongside vectors

---

## 🔐 Security Best Practices

- Never commit API keys to version control
- Use service accounts with limited permissions when possible
- Implement proper error handling for authentication failures
- Consider using environment-specific indexes for development/production

---

## 📚 Additional Resources

- [Pinecone Documentation](https://docs.pinecone.io/)
- [Embedding Model Compatibility Guide](https://docs.pinecone.io/docs/openai)
- [Pinecone Python Client](https://github.com/pinecone-io/pinecone-python-client)

---

<div align="center">
    <p><strong>Pinecone MCP Server</strong> - Vector search for intelligent AI</p>
</div>
