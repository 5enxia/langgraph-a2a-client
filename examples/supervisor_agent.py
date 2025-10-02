import asyncio

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from langgraph_a2a_client import A2AClientToolProvider

provider = A2AClientToolProvider(
    known_agent_urls=[
        "http://localhost:9000",
        "http://localhost:9001",
    ]
)


llm = ChatOpenAI(model="gpt-4.1")
agent = create_react_agent(
    model=llm,
    tools=provider.tools,
    prompt=("You are a team supervisor managing a coding agent and a weather information agent."),
    name="supervisor",
    checkpointer=MemorySaver(),
)


async def main():
    config = RunnableConfig(configurable={"thread_id": 1})
    response = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(content="How is the weather in New York City?"),
            ]
        },
        config=config,
    )
    messages = response["messages"]
    for message in messages:
        print(message.content)

    response = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(content="Write a hello world program in Python."),
            ]
        },
        config=config,
    )
    messages = response["messages"]
    for message in messages:
        print(message.content)


asyncio.run(main())
