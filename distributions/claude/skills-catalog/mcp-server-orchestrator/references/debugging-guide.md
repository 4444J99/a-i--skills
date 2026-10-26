# MCP Debugging Guide

## Diagnostic Checklist

### 1. Configuration Validation

```bash
# Validate JSON syntax
python3 -c "import json; json.load(open('claude_desktop_config.json'))"

# Pretty-print config
python3 -m json.tool claude_desktop_config.json
```

**Common JSON errors:**
- Trailing commas (not allowed in JSON)
- Missing quotes around keys
- Wrong quote characters (use `"` not `'`)

### 2. Server Startup Test

Test server independently before integrating:

```bash
# Python server
python -m my_server 2>&1

# Node server  
npx -y @scope/package-name 2>&1

# With environment variables
API_KEY=test python -m my_server <!-- allow-secret -->
```

**Expected output:** Server should start without errors and wait for input.

### 3. Log Locations

| Client | Log Path |
|--------|----------|
| Claude Desktop (macOS) | `~/Library/Logs/Claude/mcp*.log` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\logs\mcp*.log` |
| Claude Code | Output panel → "MCP Servers" |

```bash
# Tail Claude Desktop logs
tail -f ~/Library/Logs/Claude/mcp*.log

# Search for errors
grep -i error ~/Library/Logs/Claude/mcp*.log
```

### 4. Common Issues & Solutions

#### Server Not Starting

**Symptom:** Server appears in client but no tools available

**Causes:**
1. Wrong command path
2. Missing dependencies
3. Environment variables not set

**Solution:**
```json
{
  "my-server": {
    "command": "/absolute/path/to/python3",
    "args": ["-m", "my_server"],
    "env": {
      "PATH": "/usr/local/bin:/usr/bin"
    }
  }
}
```

#### Connection Timeout

**Symptom:** "Connection timed out" in logs

**Causes:**
1. Server crashes on startup
2. Server doesn't respond to initialize
3. Firewall blocking connection

**Debug:**
```bash
# Test MCP handshake manually
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | python -m my_server
```

#### Tool Not Found

**Symptom:** Client doesn't see expected tools

**Causes:**
1. Tool not registered properly
2. Server returning malformed response
3. Tool schema validation error

**Debug in Python:**
```python
# Test tool listing
from my_server import mcp
print(mcp.list_tools())
```

#### Authentication Failures

**Symptom:** 401/403 errors in logs

**Causes:**
1. API key not set or expired
2. Token refresh failed
3. Wrong credential format

**Solution:**
```json
{
  "my-server": {
    "env": {
      "API_KEY": "actual-key-not-placeholder"
    }
  }
}
```

### 5. JSON-RPC Debugging

Enable verbose logging in your server:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Log all incoming requests
@mcp.tool()
def debug_tool(input: str) -> str:
    logging.debug(f"Received input: {input}")
    return "ok"
```

### 6. Transport Issues

#### stdio Transport

Most common transport. Issues often caused by:
- Server writing to stdout (use stderr for logs)
- Buffering issues
- Encoding problems

```python
# Always use stderr for debug output
import sys
print("Debug message", file=sys.stderr)
```

#### SSE Transport

For web-based servers:
- Check CORS headers
- Verify endpoint URL accessible
- Check for proxy issues

### 7. Restart Procedures

After config changes:

1. **Claude Desktop**: Quit completely (Cmd+Q / Alt+F4), restart
2. **Claude Code**: Reload window (Cmd+Shift+P → "Reload Window")
3. **Server**: Kill existing processes before restart

```bash
# Kill orphaned Python MCP servers
pkill -f "python.*mcp"

# Kill orphaned Node MCP servers  
pkill -f "node.*mcp"
```

### 8. Testing Tools

#### MCP Inspector

```bash
# Install MCP inspector
npm install -g @modelcontextprotocol/inspector

# Run against your server
mcp-inspector python -m my_server
```

#### Manual Testing Script

```python
#!/usr/bin/env python3
"""Test MCP server manually."""
import subprocess
import json

def send_request(proc, method, params=None):
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    proc.stdin.write(json.dumps(request) + "\n")
    proc.stdin.flush()
    response = proc.stdout.readline()
    return json.loads(response)

# Start server
proc = subprocess.Popen(
    ["python", "-m", "my_server"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

# Test initialize
resp = send_request(proc, "initialize", {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "test", "version": "1.0"}
})
print("Initialize:", resp)

# Test list tools
resp = send_request(proc, "tools/list")
print("Tools:", resp)

proc.terminate()
```
