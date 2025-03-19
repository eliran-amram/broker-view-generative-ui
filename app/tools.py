from administration_service_sdk import DefaultApi, init_api, ApiException
from langchain_core.tools import tool, Tool
from pydantic import BaseModel

global model, serp_api, tool_node, admin_service

@tool
def admin_service_is_up() -> bool:
    """Check that administration service is accessible."""
    try:
        return admin_service.health_check().healthy
    except ApiException:
        return False

@tool
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
