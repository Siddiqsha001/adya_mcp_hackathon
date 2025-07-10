# Abstract API MCP Server - Credentials Setup

<div align="center">
    <img src="https://www.abstractapi.com/static/social-card.png" width="300" alt="Abstract API Logo">
    <h2>Configuring Authentication for Abstract API MCP Server</h2>
</div>

---

## 🔑 API Key Requirements

To use the Abstract API MCP Server, you need to obtain an API key from Abstract API. This key allows you to access their various data validation services.

---

## 📝 How to Get an API Key

1. **Create an Account**: Visit [Abstract API](https://www.abstractapi.com/) and sign up for an account
2. **Choose Services**: Select which validation services you need (email, phone, etc.)
3. **Get Your API Key**: From your dashboard, locate and copy your API key

---

## ⚙️ Server Configuration

The Abstract API MCP Server requires your API key to be set in the environment. You can configure this in two ways:

### Option 1: Environment Variables

Create a `.env` file in the root directory of the abstract-api-mcp-server with the following content:

```
ABSTRACT_API_KEY=your_api_key_here
```

### Option 2: Direct Configuration

You can also set the API key directly in the server configuration:

1. Open `c:\Users\siddi\OneDrive\Desktop\final\adya_mcp_hackathon-main\mcp_servers\python\servers\abstractapi-mcp-server\server.py`
2. Locate the line with `ABSTRACT_API_KEY = os.getenv("ABSTRACT_API_KEY", "your_api_key_here")`
3. Replace `"your_api_key_here"` with your actual API key

---

## 🔍 Verifying Credentials

To verify your API key is working correctly:

1. Start the Abstract API MCP Server
2. Try running a simple email validation test
3. Check that you receive a proper response without authentication errors

---

## 📊 API Usage and Limits

- Free tier: Limited requests per month
- Paid tiers: Various limits based on your subscription
- Monitor your usage through the Abstract API dashboard

---

## 🔐 Security Best Practices

- Never commit your API key to version control
- Rotate your API keys periodically
- Use environment variables for key management
- Implement rate limiting to prevent accidental overuse

---

<div align="center">
    <p><strong>Abstract API MCP Server</strong> - Secure and effective data validation</p>
</div>
