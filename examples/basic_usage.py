"""
Example usage of LangGraph A2A Client.

This example demonstrates how to use the A2A Client tool provider
in a LangGraph application.
"""

import asyncio
from langgraph_a2a_client import A2AClientToolProvider


async def main():
    """Main example function."""

    # Initialize the A2A client with known agent URLs
    a2a_client = A2AClientToolProvider(
        known_agent_urls=[
            "http://127.0.0.1:9000",
        ],
        timeout=300,
        # Optional: Configure webhook for push notifications
        # webhook_url="https://your-webhook.com/notify",
        # webhook_token="your-webhook-token",
    )

    # Get the tools for use in LangGraph
    tools = a2a_client.tools
    print(f"Available tools: {[tool.name for tool in tools]}")

    # Example 1: Discover a new agent
    print("\n=== Example 1: Discover Agent ===")
    discover_result = await a2a_client.a2a_discover_agent(url="http://127.0.0.1:9001")
    print(f"Discovery result: {discover_result['status']}")
    if discover_result["status"] == "success":
        agent_card = discover_result["agent_card"]
        print(f"Agent name: {agent_card.get('name', 'N/A')}")
        print(f"Agent description: {agent_card.get('description', 'N/A')}")

    # Example 2: List all discovered agents
    print("\n=== Example 2: List Discovered Agents ===")
    list_result = await a2a_client.a2a_list_discovered_agents()
    print(f"Status: {list_result['status']}")
    print(f"Total agents: {list_result['total_count']}")
    if list_result["status"] == "success":
        for i, agent in enumerate(list_result["agents"], 1):
            print(f"{i}. {agent.get('name', 'Unknown')} - {agent.get('url', 'N/A')}")

    # Example 3: Send a message to an agent
    print("\n=== Example 3: Send Message ===")
    send_result = await a2a_client.a2a_send_message(
        message_text="Hello, please help me with a task",
        target_agent_url="http://127.0.0.1:9000",
        message_id="example-message-001",
    )
    print(f"Send status: {send_result['status']}")
    if send_result["status"] == "success":
        print(f"Message ID: {send_result['message_id']}")
        print(f"Response: {send_result['response']}")
    else:
        print(f"Error: {send_result.get('error', 'Unknown error')}")

    # Clean up
    await a2a_client.close()


if __name__ == "__main__":
    print("=== LangGraph A2A Client Example ===\n")
    asyncio.run(main())
