# Portainer MCP Server – Demos and Payload Examples

## 🎥 Demo Video
- **MCP server setup explanation + API Gathering + Features Testing**: https://drive.google.com/drive/folders/1V4SD_cCecPHiw3ys_71bo0KyR-dHQWw0

---

## 🔐 Credential JSON Payload
Example payload format for sending credentials to the MCP Server:
```json
{
  "PORTAINER": {
    "PORTAINER_API": "https://portainer.example.com/api",
    "PORTAINER_USERNAME": "admin",
    "PORTAINER_PASSWORD": "your-secure-password"
  }
}
```

## 📋 Example Tool Calls

### List All Containers
```python
response = await session.execute("list_portainer_containers")
print(response)
```

### Start a Container
```python
container_id = "abc123def456"
response = await session.execute("start_container", {"container_id": container_id})
print(response)
```

### Stop a Container
```python
container_id = "abc123def456"
response = await session.execute("stop_container", {"container_id": container_id})
print(response)
```

### Get Container Logs
```python
container_id = "abc123def456"
response = await session.execute("get_container_logs", {"container_id": container_id})
print(response)
```
