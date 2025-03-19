"""
Please DO NOT modify this file !!!
"""
import logging
import os
import uuid
from datetime import datetime, timezone
from functools import partial

from atbay_bootstrap import start_app as start_base_app
from atbay_logger import Logger
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from app.errors.handlers import ERROR_HANDLERS
from app.prompts import SYSTEM_INSTRUCTIONS
from app.tools import web_search, admin_service_is_up, search_teams_by_name_handler, ask_human_tool
from app.utils import load_environment_variables, setup_model, setup_serp_api, create_workflow, setup_initial_messages

from administration_service_sdk import DefaultApi, init_api

def init_app():
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


Logger.init_default_logger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

start_app = partial(
    start_base_app, errors_handlers=ERROR_HANDLERS, custom_plugin_location='app/plugins'
)

# init_app()

