# Abstract API MCP Server

A Model Context Protocol (MCP) server that provides email and phone validation tools using Abstract API services. This server is built with FastMCP, making it easy to integrate validation capabilities into AI applications and workflows.

## Overview

This MCP server exposes three main validation tools:
- **Email Validation**: Comprehensive email address validation and verification
- **Phone Validation**: Phone number validation for 190+ countries
- **Email Reputation**: Advanced email reputation analysis with security insights

## Features

### Email Validation
- Format validation
- Deliverability checking
- Domain verification
- SMTP validation
- Detection of disposable/role/catchall emails
- Quality scoring

### Phone Validation
- International phone number validation
- Format standardization (international/local)
- Country and carrier identification
- Phone type detection (mobile, landline, etc.)
- Location information

### Email Reputation
- Comprehensive deliverability analysis
- Quality scoring and risk assessment
- Sender and organization identification
- Domain security analysis (DMARC, SPF)
- Data breach history tracking
- Fraud and abuse detection

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (fast Python package installer)
- Abstract API key (get one at [abstractapi.com](https://abstractapi.com))

## Installation

### Option 1: Using uv (Recommended)


2. Clone the repository:
```bash
git clone https://github.com/avivshafir/abstractapi-mcp-server
cd abstractapi-mcp-server
```

3. Create virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install .
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Abstract API key
```

### Option 2: Using traditional pip

1. Clone the repository:
```bash
git clone https://github.com/avivshafir/abstractapi-mcp-server
cd abstractapi-mcp-server
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Abstract API key
```

Your `.env` file should contain:
```
ABSTRACT_API_KEY=your_abstract_api_key_here
```

## Usage

### Running the MCP Server

The server can be run in stdio mode for integration with MCP clients:

```bash
# With uv (if virtual environment is activated)
python server.py

# Or run directly with uv
uv run server.py
```

### FastMCP Framework

This server is built using [FastMCP](https://github.com/jlowin/fastmcp), a Python framework that simplifies MCP server development. FastMCP provides:

- **Automatic tool registration**: Functions decorated with `@mcp.tool()` are automatically exposed as MCP tools
- **Type safety**: Full type hints and validation
- **Easy async support**: Native async/await support
- **Simplified server setup**: Minimal boilerplate code

#### Key FastMCP Concepts

```python
from mcp.server.fastmcp import FastMCP

# Initialize the server
mcp = FastMCP("abstract_api")

# Register a tool
@mcp.tool()
async def my_tool(param: str) -> dict:
    """Tool description for AI clients"""
    return {"result": param}

# Run the server
mcp.run(transport="stdio")
```

### Available Tools

#### 1. Email Validation (`verify_email`)

Validates email addresses and returns comprehensive information.

**Parameters:**
- `email` (str): Email address to validate

**Example Response:**
```json
{
  "email": "user@example.com",
  "deliverability": "DELIVERABLE",
  "quality_score": "0.99",
  "is_valid_format": {"value": true, "text": "TRUE"},
  "is_free_email": {"value": false, "text": "FALSE"},
  "is_disposable_email": {"value": false, "text": "FALSE"},
  "is_role_email": {"value": false, "text": "FALSE"},
  "is_catchall_email": {"value": false, "text": "FALSE"},
  "is_mx_found": {"value": true, "text": "TRUE"},
  "is_smtp_valid": {"value": true, "text": "TRUE"}
}
```

#### 2. Phone Validation (`validate_phone`)

Validates phone numbers from 190+ countries.

**Parameters:**
- `phone` (str): Phone number to validate
- `country` (str, optional): ISO country code for context

**Example Response:**
```json
{
  "phone": "14152007986",
  "valid": true,
  "format": {
    "international": "+14152007986",
    "local": "(415) 200-7986"
  },
  "country": {
    "code": "US",
    "name": "United States",
    "prefix": "+1"
  },
  "location": "California",
  "type": "mobile",
  "carrier": "T-Mobile USA, Inc."
}
```

#### 3. Email Reputation (`check_email_reputation`)

Provides comprehensive email reputation analysis including security insights and breach history.

**Parameters:**
- `email` (str): Email address to analyze

**Example Response:**
```json
{
  "email_address": "benjamin.richard@abstractapi.com",
  "email_deliverability": {
    "status": "deliverable",
    "status_detail": "valid_email",
    "is_format_valid": true,
    "is_smtp_valid": true,
    "is_mx_valid": true,
    "mx_records": ["gmail-smtp-in.l.google.com", "..."]
  },
  "email_quality": {
    "score": 0.8,
    "is_free_email": false,
    "is_username_suspicious": false,
    "is_disposable": false,
    "is_catchall": true,
    "is_subaddress": false,
    "is_role": false,
    "is_dmarc_enforced": true,
    "is_spf_strict": true,
    "minimum_age": 1418
  },
  "email_sender": {
    "first_name": "Benjamin",
    "last_name": "Richard",
    "email_provider_name": "Google",
    "organization_name": "Abstract API",
    "organization_type": "company"
  },
  "email_domain": {
    "domain": "abstractapi.com",
    "domain_age": 1418,
    "is_live_site": true,
    "registrar": "NAMECHEAP INC",
    "date_registered": "2020-05-13",
    "date_expires": "2025-05-13",
    "is_risky_tld": false
  },
  "email_risk": {
    "address_risk_status": "low",
    "domain_risk_status": "low"
  },
  "email_breaches": {
    "total_breaches": 2,
    "date_first_breached": "2018-07-23T14:30:00Z",
    "date_last_breached": "2019-05-24T14:30:00Z",
    "breached_domains": [
      {"domain": "apollo.io", "date_breached": "2018-07-23T14:30:00Z"},
      {"domain": "canva.com", "date_breached": "2019-05-24T14:30:00Z"}
    ]
  }
}
```

## Integration with MCP Clients

Add this server to your mcp configuration:

```json
{
  "mcpServers": {
    "abstract-api": {
      "command": "uv",
      "args": ["run", "/path/to/mcp-abstract-api/server.py"],
      "env": {
        "ABSTRACT_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Alternatively, if you prefer to use the traditional approach:

```json
{
  "mcpServers": {
    "abstract-api": {
      "command": "python",
      "args": ["/path/to/mcp-abstract-api/server.py"],
      "env": {
        "ABSTRACT_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Other MCP Clients

This server follows the standard MCP protocol and can be integrated with any MCP-compatible client. The server communicates via stdio transport.

## Error Handling

The server includes comprehensive error handling:

- **API Key Validation**: Checks for missing API keys
- **HTTP Error Handling**: Proper handling of API response errors
- **Input Validation**: Type checking and parameter validation
- **Graceful Degradation**: Meaningful error messages for debugging

## API Rate Limits

Abstract API has different rate limits based on your plan:
- Free plans: 1 request per second
- Paid plans: Higher rate limits available

Each API call counts as one credit, regardless of whether the validation succeeds or fails.

## Development

### Project Structure

```
mcp-abstract-api/
├── server.py          # Main MCP server implementation
├── .env              # Environment variables (not in repo)
├── .env.example      # Environment template
├── requirements.txt  # Python dependencies (pip format)
├── uv.lock           # uv lock file for reproducible builds
├── pyproject.toml    # Project configuration
├── README.md         # This file
└── LICENSE          # MIT License
```

### Adding New Tools

To add new Abstract API tools:

1. Add the API endpoint URL as a constant
2. Create a new function decorated with `@mcp.tool()`
3. Add comprehensive docstring with parameter and return descriptions
4. Implement error handling following the existing pattern

Example:
```python
@mcp.tool()
async def new_validation_tool(param: str) -> dict[str, Any]:
    """
    Description of what this tool does.
    
    Args:
        param (str): Description of parameter
        
    Returns:
        dict[str, Any]: Description of return value
    """
    # Implementation here
    pass
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues related to:
- **This MCP server**: Open an issue in this repository
- **Abstract API**: Contact [Abstract API support](https://abstractapi.com/contact)
- **FastMCP framework**: Check the [FastMCP documentation](https://github.com/jlowin/fastmcp)

## Acknowledgments

- [Abstract API](https://abstractapi.com) for providing the validation services
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server framework
- [Model Context Protocol](https://modelcontextprotocol.io/) for the protocol specification
