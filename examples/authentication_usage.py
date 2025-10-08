"""
Example usage of LangGraph A2A Client with Authentication.

This example demonstrates how to use the A2A Client tool provider
with various authentication methods.
"""

import asyncio
import httpx
from langgraph_a2a_client import A2AClientToolProvider


async def example_api_key_auth():
    """Example: Using API Key authentication via headers."""
    print("\n=== Example 1: API Key Authentication ===")
    
    a2a_client = A2AClientToolProvider(
        known_agent_urls=["http://127.0.0.1:9000"],
        timeout=300,
        headers={"X-API-Key": "your-api-key-here"}
    )
    
    print("✓ A2A Client initialized with API Key authentication")
    
    # Use the tools
    tools = a2a_client.tools
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    await a2a_client.close()


async def example_bearer_token_auth():
    """Example: Using Bearer token authentication via headers."""
    print("\n=== Example 2: Bearer Token Authentication ===")
    
    a2a_client = A2AClientToolProvider(
        known_agent_urls=["http://127.0.0.1:9000"],
        timeout=300,
        headers={"Authorization": "Bearer your-token-here"}
    )
    
    print("✓ A2A Client initialized with Bearer token authentication")
    
    # Use the tools
    tools = a2a_client.tools
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    await a2a_client.close()


async def example_basic_auth():
    """Example: Using Basic authentication."""
    print("\n=== Example 3: Basic Authentication ===")
    
    # Option 1: Using tuple shorthand
    a2a_client = A2AClientToolProvider(
        known_agent_urls=["http://127.0.0.1:9000"],
        timeout=300,
        auth=("username", "password")
    )
    
    print("✓ A2A Client initialized with Basic authentication (tuple)")
    await a2a_client.close()
    
    # Option 2: Using httpx.BasicAuth
    a2a_client = A2AClientToolProvider(
        known_agent_urls=["http://127.0.0.1:9000"],
        timeout=300,
        auth=httpx.BasicAuth("username", "password")
    )
    
    print("✓ A2A Client initialized with Basic authentication (httpx.BasicAuth)")
    
    # Use the tools
    tools = a2a_client.tools
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    await a2a_client.close()


async def example_custom_headers():
    """Example: Using multiple custom headers."""
    print("\n=== Example 4: Multiple Custom Headers ===")
    
    a2a_client = A2AClientToolProvider(
        known_agent_urls=["http://127.0.0.1:9000"],
        timeout=300,
        headers={
            "X-API-Key": "your-api-key",
            "X-Client-ID": "client-123",
            "X-Custom-Header": "custom-value"
        }
    )
    
    print("✓ A2A Client initialized with multiple custom headers")
    
    # Use the tools
    tools = a2a_client.tools
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    await a2a_client.close()


async def example_combined_auth():
    """Example: Using both headers and auth together."""
    print("\n=== Example 5: Combined Headers and Auth ===")
    
    a2a_client = A2AClientToolProvider(
        known_agent_urls=["http://127.0.0.1:9000"],
        timeout=300,
        headers={"X-API-Key": "your-api-key"},
        auth=("username", "password")
    )
    
    print("✓ A2A Client initialized with both custom headers and Basic auth")
    
    # Use the tools
    tools = a2a_client.tools
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    await a2a_client.close()


async def main():
    """Run all authentication examples."""
    print("=== LangGraph A2A Client Authentication Examples ===")
    
    await example_api_key_auth()
    await example_bearer_token_auth()
    await example_basic_auth()
    await example_custom_headers()
    await example_combined_auth()
    
    print("\n=== All examples completed ===")


if __name__ == "__main__":
    asyncio.run(main())
