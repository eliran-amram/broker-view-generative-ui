from typing import List, Union, Dict, Any

from dotenv import load_dotenv, find_dotenv
from langchain_aws import ChatBedrockConverse
from botocore.config import Config
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langgraph.graph import MessagesState, START, END, StateGraph

from app.prompts import INITIAL_GREETING

global model, serp_api, tool_node, admin_service


def load_environment_variables() -> None:
    load_dotenv(find_dotenv())


def setup_model() -> ChatBedrockConverse:
    bedrock_config = Config(read_timeout=1000)
    return ChatBedrockConverse(
        model='anthropic.claude-3-5-sonnet-20240620-v1:0',
        config=bedrock_config,
        temperature=0.0,
        top_p=1.0
    )


def setup_serp_api() -> SerpAPIWrapper:
    params = {
        "engine": "google",
        "gl": "us",
        "hl": "en",
    }
    return SerpAPIWrapper(params=params)


def should_continue(state: Dict[str, Any]) -> str:
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"


def call_model(state: Dict[str, Any]) -> Dict[str, List[Any]]:
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}


def create_workflow() -> StateGraph:
    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", call_model)
    workflow.add_node("action", tool_node)
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "action",
            "end": END,
        },
    )
    workflow.add_edge("action", "agent")
    return workflow


def setup_initial_messages(system_instructions: str) -> List[Union[SystemMessage, HumanMessage]]:
    return [
        SystemMessage(content=system_instructions),
        HumanMessage(content=INITIAL_GREETING)
    ]

