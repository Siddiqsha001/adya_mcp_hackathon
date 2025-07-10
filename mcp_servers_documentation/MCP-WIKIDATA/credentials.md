# Wikidata MCP Server Credentials

## Overview
This document provides information about credentials for the Wikidata MCP Server. The Wikidata API is publicly accessible and generally does not require authentication for basic queries.

---

## Credential Format
```json
{
  "WIKIDATA": {
    "USER_AGENT": "your-application-name/version (your-contact-email)"
  }
}
```

## Notes on Wikidata Access

1. **No Authentication Required**: Most Wikidata API operations don't require authentication
   - Basic SPARQL queries and entity searches can be performed anonymously
   - Rate limits apply to unauthenticated requests

2. **User Agent**: While optional, it's good practice to identify your application
   - Include your application name and version
   - Provide a contact email for Wikimedia operators if needed

3. **For Advanced Usage**:
   - If you need to perform write operations or need higher rate limits
   - Create a Wikimedia account at [https://www.wikidata.org/](https://www.wikidata.org/)
   - Follow OAuth authentication procedures documented at [https://www.mediawiki.org/wiki/OAuth/For_Developers](https://www.mediawiki.org/wiki/OAuth/For_Developers)

4. **Usage Policies**:
   - Respect Wikimedia Foundation's [Terms of Use](https://foundation.wikimedia.org/wiki/Terms_of_Use)
   - Follow [Bot Policy](https://www.wikidata.org/wiki/Wikidata:Bots) for automated access
