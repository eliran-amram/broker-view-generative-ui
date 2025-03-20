from typing import List, Union, Dict, Any

from dotenv import load_dotenv, find_dotenv
from langchain_aws import ChatBedrockConverse
from botocore.config import Config
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langgraph.graph import MessagesState, START, END, StateGraph

from app.plugins.globals import AppGlobals
from app.prompts import INITIAL_GREETING, SYSTEM_INSTRUCTIONS
from atbay_bootstrap import signals


def load_environment_variables() -> None:
    load_dotenv(find_dotenv())


def setup_model() -> ChatBedrockConverse:
    bedrock_config = Config(read_timeout=1000)
    return ChatBedrockConverse(
        model='us.anthropic.claude-3-5-sonnet-20241022-v2:0',
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
    response = AppGlobals.model.invoke(messages)
    return {"messages": [response]}


def create_workflow() -> StateGraph:
    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", call_model)
    workflow.add_node("action", AppGlobals.tool_node)
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


def init_agent_for_convos(app: Any, config: Dict[str, Any], initial_messages: List[Union[SystemMessage, HumanMessage]]):
    # Start the conversation
    for event in app.stream({"messages": initial_messages}, config, stream_mode="values"):
        if type(event["messages"][-1]) != AIMessage:
            continue
        elif event["messages"][-1].content == 'ready':
            #print(f'{type(event["messages"][-1].content)}')
            print(f'{event["messages"][-1].content}')


@signals.after_boot
def init_app():
    import uuid
    import logging
    from datetime import datetime, timezone

    load_environment_variables()

    AppGlobals.init_globals()

    thread_id = str(uuid.uuid4())
    logging.info(f"Thread ID: {thread_id}")
    config = {"configurable": {"thread_id": 1}}  # TODO: this should be legit id

    current_date_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    system_instructions = SYSTEM_INSTRUCTIONS.format(current_date_utc=current_date_utc)
    initial_messages = setup_initial_messages(system_instructions)

    init_agent_for_convos(AppGlobals.app, config, initial_messages)
