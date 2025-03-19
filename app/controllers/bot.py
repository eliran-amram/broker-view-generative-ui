import logging
import os
import uuid
from typing import List, Dict, Any, Union
from datetime import datetime, timezone
from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter, Request
from langchain_aws import ChatBedrockConverse
from botocore.config import Config
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import tool, Tool
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langgraph.graph import MessagesState, START, END, StateGraph
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel
from administration_service_sdk import DefaultApi, init_api, ApiException

from app.prompts import INITIAL_GREETING, SYSTEM_INSTRUCTIONS

router = APIRouter(prefix="/bot")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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


def admin_service_is_up() -> bool:
    """Check that administration service is accessible."""
    try:
        return admin_service.health_check().healthy
    except ApiException:
        return False


def search_teams_by_name_handler(search_name: str) -> list:
    """Search administration service for teams by their name."""
    try:
        return admin_service.search_brokerage_entities(search_term=search_name, entity_name=["TEAM"]).data.teams
    except ApiException:
        return []


@tool
def web_search(query: str) -> str:
    """Search the web for the given query using Google (accepts Google search syntax)."""
    return serp_api.run(query)


class AskHuman(BaseModel):
    """Ask the human a question"""
    question: str


def ask_human_func(question: str) -> str:
    """Ask the human a question and get their input."""
    return input(f"{question}\nYour response: ")


ask_human_tool = Tool(
    name="AskHuman",
    func=ask_human_func,
    description="Ask the human a question and get their input.",
    args_schema=AskHuman
)


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


def run_conversation(app: Any, config: Dict[str, Any], initial_messages: List[Union[SystemMessage, HumanMessage]]):
    # Start the conversation
    for event in app.stream({"messages": initial_messages}, config, stream_mode="values"):
        event["messages"][-1].pretty_print()

    # Continue with the interaction loop
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("AI: Goodbye! Have a great day!")
            break

        user_message = HumanMessage(content=user_input)
        for event in app.stream({"messages": [user_message]}, config, stream_mode="values"):
            event["messages"][-1].pretty_print()

    print('Conversation ended.')
    print('Snowflake Copilot execution completed!')


@router.get('/ask', operation_id='ask_bot', response_model_exclude_unset=True)
async def ask_bot(request: Request):
    print(request.app)
    main()


def main():
    global model, serp_api, tool_node, admin_service

    load_environment_variables()
    model = setup_model()
    serp_api = setup_serp_api()
    admin_service = init_api(api=DefaultApi, host=os.getenv('ADMIN_SERVICE_HOST'))

    tools = [web_search, admin_service_is_up, search_teams_by_name_handler, ask_human_tool]

    tool_node = ToolNode(tools)
    model = model.bind_tools(tools)

    workflow = create_workflow()
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    thread_id = str(uuid.uuid4())
    logger.info(f"Thread ID: {thread_id}")
    config = {"configurable": {"thread_id": thread_id}}

    current_date_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    system_instructions = SYSTEM_INSTRUCTIONS.format(current_date_utc=current_date_utc)
    initial_messages = setup_initial_messages(system_instructions)

    run_conversation(app, config, initial_messages)
