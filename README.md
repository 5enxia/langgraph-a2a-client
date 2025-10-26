# LangGraph A2A Client

A2A (Agent-to-Agent) Protocol Client Tool for LangGraph.

## Overview

This library provides functionality to discover and communicate with A2A-compliant agents in LangGraph applications.

## Key Features

- Agent discovery through agent cards from multiple URLs
- Message sending to specific A2A agents
- LangChain tool integration for easy use in LangGraph workflows

## Installation

```bash
pip install langgraph-a2a-client
```

Or with uv:

```bash
uv add langgraph-a2a-client
```

## Usage

```python
from langgraph_a2a_client import A2AClientToolProvider

# Initialize the A2A client
a2a_client = A2AClientToolProvider(
    known_agent_urls=["https://example.com/agent"],
    timeout=300,
    webhook_url="https://your-webhook.com/notify",
    webhook_token="your-webhook-token",
    headers={
        "https://example.com/agent": {"X-API-Key": "your-api-key"}
    }  # Optional: Per-URL headers for authentication
)

# Get the tools for use in LangGraph
tools = a2a_client.tools

# Use in your LangGraph application
# ...
```

## API

### A2AClientToolProvider

Main class that provides A2A client functionality.

#### Parameters

- `known_agent_urls` (list[str] | None): List of A2A agent URLs to discover initially
- `timeout` (int): Timeout for HTTP operations in seconds (default: 300)
- `webhook_url` (str | None): Optional webhook URL for push notifications
- `webhook_token` (str | None): Optional authentication token for webhook notifications
- `headers` (dict[str, dict[str, str]] | None): Optional per-URL HTTP headers for authentication. Format: `{"https://agent-url.com": {"X-API-Key": "key", "Authorization": "Bearer token"}}`

#### Tools

The provider exposes three tools:

1. **a2a_discover_agent**: Discover an A2A agent and return its agent card
2. **a2a_list_discovered_agents**: List all discovered A2A agents and their capabilities
3. **a2a_send_message**: Send a message to a specific A2A agent

### Authentication

The client supports configuring HTTP headers per agent URL for authentication:

#### API Key Authentication (Per URL)

```python
a2a_client = A2AClientToolProvider(
    known_agent_urls=["https://agent1.example.com", "https://agent2.example.com"],
    headers={
        "https://agent1.example.com": {"X-API-Key": "api-key-for-agent1"},
        "https://agent2.example.com": {"X-API-Key": "api-key-for-agent2"}
    }
)
```

#### Bearer Token Authentication

```python
a2a_client = A2AClientToolProvider(
    known_agent_urls=["https://example.com/agent"],
    headers={
        "https://example.com/agent": {"Authorization": "Bearer your-token"}
    }
)
```

#### Custom Headers (Per URL)

```python
a2a_client = A2AClientToolProvider(
    known_agent_urls=["https://example.com/agent"],
    headers={
        "https://example.com/agent": {
            "X-Custom-Header": "custom-value",
            "X-Client-ID": "client-123",
            "Authorization": "Bearer token"
        }
    }
)
```

#### Multiple Agents with Different Authentication

```python
a2a_client = A2AClientToolProvider(
    known_agent_urls=[
        "https://public-agent.example.com",
        "https://secure-agent.example.com"
    ],
    headers={
        # Secure agent requires authentication
        "https://secure-agent.example.com": {
            "X-API-Key": "secret-key",
            "X-Tenant-ID": "tenant-123"
        }
        # Public agent has no entry, so no headers are added
    }
)
```

## Examples

### Basic Usage

```sh
uv run examples/basic_usage.py
```

### Authentication Usage

```sh
uv run examples/authentication_usage.py
```

### Supervisor Agent Example

```sh
export OPENAI_API_KEY="your-openai-api"
uv run --extra examples examples/supervisor_agent.py
```

## License

MIT
