"""Tests for A2A Client Tool Provider."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from langgraph_a2a_client import A2AClientToolProvider


@pytest.fixture
def mock_agent_card():
    """Mock agent card for testing."""
    return MagicMock(
        name="Test Agent",
        description="A test agent",
        url="https://example.com/agent",
        model_dump=MagicMock(
            return_value={
                "name": "Test Agent",
                "description": "A test agent",
                "url": "https://example.com/agent",
            }
        ),
    )


@pytest.fixture
async def a2a_client():
    """Create A2A client for testing."""
    client = A2AClientToolProvider(
        known_agent_urls=["https://example.com/agent"],
        timeout=10,
    )
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_initialization():
    """Test A2A client initialization."""
    client = A2AClientToolProvider(
        known_agent_urls=["https://example.com/agent1", "https://example.com/agent2"],
        timeout=60,
        webhook_url="https://webhook.example.com",
        webhook_token="test-token",
    )

    assert client.timeout == 60
    assert len(client._known_agent_urls) == 2
    assert client._webhook_url == "https://webhook.example.com"
    assert client._webhook_token == "test-token"
    assert client._push_config is not None

    await client.close()


@pytest.mark.asyncio
async def test_tools_property(a2a_client):
    """Test that tools property returns LangChain StructuredTool instances."""
    tools = a2a_client.tools

    assert len(tools) == 3
    assert all(tool.__class__.__name__ == "StructuredTool" for tool in tools)

    tool_names = [tool.name for tool in tools]
    assert "a2a_discover_agent" in tool_names
    assert "a2a_list_discovered_agents" in tool_names
    assert "a2a_send_message" in tool_names


@pytest.mark.asyncio
async def test_discover_agent_success(a2a_client, mock_agent_card):
    """Test successful agent discovery."""
    with patch.object(a2a_client, "_discover_agent_card", new_callable=AsyncMock) as mock_discover:
        mock_discover.return_value = mock_agent_card

        result = await a2a_client.a2a_discover_agent("https://example.com/new-agent")

        assert result["status"] == "success"
        assert result["url"] == "https://example.com/new-agent"
        assert "agent_card" in result
        # Check that it was called with the new URL (may be called multiple times due to initialization)
        mock_discover.assert_any_call("https://example.com/new-agent")


@pytest.mark.asyncio
async def test_discover_agent_error(a2a_client):
    """Test agent discovery error handling."""
    with patch.object(a2a_client, "_discover_agent_card", new_callable=AsyncMock) as mock_discover:
        mock_discover.side_effect = Exception("Connection error")

        result = await a2a_client.a2a_discover_agent("https://example.com/bad-agent")

        assert result["status"] == "error"
        assert "error" in result
        assert result["url"] == "https://example.com/bad-agent"


@pytest.mark.asyncio
async def test_list_discovered_agents(a2a_client, mock_agent_card):
    """Test listing discovered agents."""
    # Add a mock agent to the cache
    a2a_client._discovered_agents["https://example.com/agent"] = mock_agent_card
    a2a_client._initial_discovery_done = True

    result = await a2a_client.a2a_list_discovered_agents()

    assert result["status"] == "success"
    assert result["total_count"] == 1
    assert len(result["agents"]) == 1


@pytest.mark.asyncio
async def test_send_message_success(a2a_client, mock_agent_card):
    """Test successful message sending."""
    # Mock the message response
    mock_message = MagicMock(model_dump=MagicMock(return_value={"content": "Response from agent"}))

    # Create an async generator for send_message
    async def mock_send_message_gen(message):
        yield mock_message

    with (
        patch.object(a2a_client, "_discover_agent_card", new_callable=AsyncMock) as mock_discover,
        patch.object(a2a_client, "_ensure_client_factory", new_callable=AsyncMock) as mock_factory,
    ):
        mock_discover.return_value = mock_agent_card

        mock_client = MagicMock()
        mock_client.send_message = MagicMock(side_effect=mock_send_message_gen)

        mock_factory_instance = MagicMock()
        mock_factory_instance.create = MagicMock(return_value=mock_client)
        mock_factory.return_value = mock_factory_instance

        result = await a2a_client.a2a_send_message(
            message_text="Hello", target_agent_url="https://example.com/agent", message_id="test-123"
        )

        assert result["status"] == "success"
        assert result["message_id"] == "test-123"
        assert result["target_agent_url"] == "https://example.com/agent"


@pytest.mark.asyncio
async def test_send_message_error(a2a_client):
    """Test message sending error handling."""
    with patch.object(a2a_client, "_discover_agent_card", new_callable=AsyncMock) as mock_discover:
        mock_discover.side_effect = Exception("Agent not found")

        result = await a2a_client.a2a_send_message(
            message_text="Hello", target_agent_url="https://example.com/bad-agent"
        )

        assert result["status"] == "error"
        assert "error" in result


@pytest.mark.asyncio
async def test_context_manager():
    """Test async context manager functionality."""
    async with A2AClientToolProvider() as client:
        assert len(client._httpx_clients) == 0  # Not initialized yet
        tools = client.tools
        assert len(tools) == 3

    # After exiting context, resources should be cleaned up
    assert len(client._httpx_clients) == 0


@pytest.mark.asyncio
async def test_ensure_httpx_client(a2a_client):
    """Test HTTP client initialization."""
    test_url = "https://example.com/agent"
    client1 = await a2a_client._ensure_httpx_client(test_url)
    client2 = await a2a_client._ensure_httpx_client(test_url)

    # Should return the same instance for the same URL
    assert client1 is client2
    assert test_url in a2a_client._httpx_clients
    assert a2a_client._httpx_clients[test_url] is not None


@pytest.mark.asyncio
async def test_authentication_with_headers():
    """Test A2A client initialization with per-URL custom headers."""
    url = "https://example.com/agent"
    headers_config = {url: {"X-API-Key": "test-api-key", "X-Client-ID": "client-123"}}
    client = A2AClientToolProvider(
        known_agent_urls=[url],
        timeout=10,
        headers=headers_config,
    )

    assert client._headers_config == headers_config

    # Verify headers are passed to httpx client for the specific URL
    httpx_client = await client._ensure_httpx_client(url)
    assert httpx_client.headers.get("X-API-Key") == "test-api-key"
    assert httpx_client.headers.get("X-Client-ID") == "client-123"

    await client.close()


@pytest.mark.asyncio
async def test_authentication_bearer_token():
    """Test A2A client initialization with Bearer token per URL."""
    url = "https://example.com/agent"
    headers_config = {url: {"Authorization": "Bearer test-token-123"}}
    client = A2AClientToolProvider(
        known_agent_urls=[url],
        timeout=10,
        headers=headers_config,
    )

    # Verify headers are passed to httpx client
    httpx_client = await client._ensure_httpx_client(url)
    assert httpx_client.headers.get("Authorization") == "Bearer test-token-123"

    await client.close()


@pytest.mark.asyncio
async def test_authentication_multiple_urls():
    """Test A2A client with different headers for different URLs."""
    url1 = "https://agent1.example.com"
    url2 = "https://agent2.example.com"
    headers_config = {
        url1: {"X-API-Key": "key-for-agent1"},
        url2: {"X-API-Key": "key-for-agent2", "X-Custom": "value"},
    }
    client = A2AClientToolProvider(
        known_agent_urls=[url1, url2],
        timeout=10,
        headers=headers_config,
    )

    # Verify each URL gets its own headers
    httpx_client1 = await client._ensure_httpx_client(url1)
    assert httpx_client1.headers.get("X-API-Key") == "key-for-agent1"
    assert httpx_client1.headers.get("X-Custom") is None

    httpx_client2 = await client._ensure_httpx_client(url2)
    assert httpx_client2.headers.get("X-API-Key") == "key-for-agent2"
    assert httpx_client2.headers.get("X-Custom") == "value"

    await client.close()

