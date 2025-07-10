# Wikidata MCP Server – Demos and Payload Examples

## 🎥 Demo Video
- **MCP server setup explanation + API Gathering + Features Testing**: https://drive.google.com/drive/folders/1dfXKuuXEQAl9_ImiP0HawgdNhrO3cRpd?usp=sharing
---

## 🔐 Credential JSON Payload
Example payload format (optional for Wikidata):
```json
{
  "WIKIDATA": {
    "USER_AGENT": "MyApp/1.0 (contact@example.com)"
  }
}
```

## 📋 Example Tool Calls

### Search for an Entity
```python
response = await session.execute("search_entity", {"query": "Bong Joon-ho"})
print(response)  # Returns: "Q495980"
```

### Search for a Property
```python
response = await session.execute("search_property", {"query": "director"})
print(response)  # Returns: "P57"
```

### Get Properties for an Entity
```python
response = await session.execute("get_properties", {"entity_id": "Q495980"})
print(response)  # Returns list of property IDs: ["P345", "P244", "P214", ...]
```

### Execute a SPARQL Query
```python
sparql_query = """
SELECT ?movie ?movieLabel WHERE {
  ?movie wdt:P57 wd:Q495980.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""
response = await session.execute("execute_sparql", {"sparql_query": sparql_query})
print(response)  # Returns movie entities directed by Bong Joon-ho
```
