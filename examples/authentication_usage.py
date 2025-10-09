"""
Example usage of LangGraph A2A Client with Authentication.

This example demonstrates how to use the A2A Client tool provider
with per-URL authentication headers.
"""

import asyncio
from langgraph_a2a_client import A2AClientToolProvider


async def example_api_key_auth():
    """Example: Using API Key authentication via headers per URL."""
    print("\n=== Example 1: API Key Authentication (Per URL) ===")
    
    url = "http://127.0.0.1:9000"
    a2a_client = A2AClientToolProvider(
        known_agent_urls=[url],
        timeout=300,
        headers={
            url: {"X-API-Key": "your-api-key-here"}
        }
    )
    
    print("✓ A2A Client initialized with API Key authentication for specific URL")
    
    # Use the tools
    tools = a2a_client.tools
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    await a2a_client.close()


async def example_bearer_token_auth():
    """Example: Using Bearer token authentication via headers per URL."""
    print("\n=== Example 2: Bearer Token Authentication ===")
    
    url = "http://127.0.0.1:9000"
    a2a_client = A2AClientToolProvider(
        known_agent_urls=[url],
        timeout=300,
        headers={
            url: {"Authorization": "Bearer your-access-token-here"}
        }
    )
    
    print("✓ A2A Client initialized with Bearer token authentication")
    
    # Use the tools
    tools = a2a_client.tools
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    await a2a_client.close()


async def example_custom_headers():
    """Example: Using multiple custom headers per URL."""
    print("\n=== Example 3: Multiple Custom Headers ===")
    
    url = "http://127.0.0.1:9000"
    a2a_client = A2AClientToolProvider(
        known_agent_urls=[url],
        timeout=300,
        headers={
            url: {
                "X-API-Key": "your-api-key",
                "X-Client-ID": "client-123",
                "X-Custom-Header": "custom-value"
            }
        }
    )
    
    print("✓ A2A Client initialized with multiple custom headers")
    
    # Use the tools
    tools = a2a_client.tools
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    await a2a_client.close()


async def example_multiple_agents():
    """Example: Different authentication for different agents."""
    print("\n=== Example 4: Multiple Agents with Different Authentication ===")
    
    agent1_url = "http://127.0.0.1:9000"
    agent2_url = "http://127.0.0.1:9001"
    
    a2a_client = A2AClientToolProvider(
        known_agent_urls=[agent1_url, agent2_url],
        timeout=300,
        headers={
            agent1_url: {"X-API-Key": "key-for-agent1"},
            agent2_url: {
                "X-API-Key": "key-for-agent2",
                "Authorization": "Bearer token-for-agent2"
            }
        }
    )
    
    print("✓ A2A Client initialized with different auth for each agent")
    print(f"  - {agent1_url}: API Key only")
    print(f"  - {agent2_url}: API Key + Bearer token")
    
    # Use the tools
    tools = a2a_client.tools
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    await a2a_client.close()


async def example_mixed_public_private():
    """Example: Mix of public and authenticated agents."""
    print("\n=== Example 5: Public and Authenticated Agents ===")
    
    public_agent = "http://127.0.0.1:9000"
    secure_agent = "http://127.0.0.1:9001"
    
    a2a_client = A2AClientToolProvider(
        known_agent_urls=[public_agent, secure_agent],
        timeout=300,
        headers={
            # Only secure agent has authentication configured
            secure_agent: {
                "X-API-Key": "secure-key",
                "X-Tenant-ID": "tenant-xyz"
            }
            # public_agent has no entry, so no headers are added
        }
    )
    
    print("✓ A2A Client initialized with mixed authentication")
    print(f"  - {public_agent}: No authentication (public)")
    print(f"  - {secure_agent}: Authenticated with API Key + Tenant ID")
    
    # Use the tools
    tools = a2a_client.tools
    print(f"Available tools: {[tool.name for tool in tools]}")
    
    await a2a_client.close()


async def main():
    """Run all authentication examples."""
    print("=== LangGraph A2A Client Authentication Examples ===")
    
    await example_api_key_auth()
    await example_bearer_token_auth()
    await example_custom_headers()
    await example_multiple_agents()
    await example_mixed_public_private()
    
    print("\n=== All examples completed ===")


if __name__ == "__main__":
    asyncio.run(main())
