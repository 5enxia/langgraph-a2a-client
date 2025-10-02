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
    webhook_token="your-webhook-token"
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

#### Tools

The provider exposes three tools:

1. **a2a_discover_agent**: Discover an A2A agent and return its agent card
2. **a2a_list_discovered_agents**: List all discovered A2A agents and their capabilities
3. **a2a_send_message**: Send a message to a specific A2A agent

## Examples

### Basic Usage

```sh
uv run examples/basic_usage.py
```

### Supervisor Agent Example

```sh
export OPENAI_API_KEY="your-openai-api"
uv run --extra examples examples/supervisor_agent.py
```

## License

MIT
