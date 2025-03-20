import logging

from administration_service_sdk import ApiException
from langchain_core.tools import tool, Tool
from pydantic import BaseModel
from nanoid import generate as generate_nano

from app.plugins.globals import AppGlobals


@tool
def admin_service_is_up() -> bool:
    """Check that administration service is accessible."""
    try:
        return AppGlobals.admin_service.health_check().healthy
    except ApiException:
        return False


@tool
def search_teams_by_name_handler(search_name: str, correlation_id: str) -> list:
    """Search administration service for teams by their name."""
    try:
        return AppGlobals.admin_service.search_brokerage_entities(
            search_term=search_name, entity_name=["TEAM"], x_correlation_id=correlation_id
        ).data.teams
    except ApiException:
        return []


@tool
def search_brokers_by_name_handler(search_name: str, correlation_id: str) -> list:
    """Search administration service for teams by their name."""
    try:
        return AppGlobals.admin_service.search_brokerage_entities(
            search_term=search_name, entity_name=["BROKER"], x_correlation_id=correlation_id
        ).data.teams
    except ApiException:
        return []


@tool
def web_search(query: str) -> str:
    """Search the web for the given query using Google (accepts Google search syntax)."""
    return AppGlobals.serp_api.run(query)


@tool
def generate_logs(message: str):
    """Use this func to log your process and steps."""
    logging.info(message)


@tool
def generate_correlation_id() -> str:
    """This function creates a random nano id."""
    return generate_nano()


def ask_human_func(question: str) -> str:
    """Ask the human a question and get their input."""
    return input(f"{question}\nYour response: ")


class AskHuman(BaseModel):
    """Ask the human a question"""
    question: str


ask_human_tool = Tool(
    name="AskHuman",
    func=ask_human_func,
    description="Ask the human a question and get their input.",
    args_schema=AskHuman
)


tools_list = [
    web_search,
    admin_service_is_up,
    search_teams_by_name_handler,
    search_brokers_by_name_handler,
    ask_human_tool,
    generate_logs
]
