import os
from typing import Any
from langchain_community.utilities import SerpAPIWrapper
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode
from administration_service_sdk import DefaultApi, init_api


class AppGlobals:
    model: Any = None
    serp_api: SerpAPIWrapper = None
    tool_node: ToolNode = None
    admin_service: Any = None  # TODO: set type
    app: CompiledStateGraph = None  # TODO: better name

    @classmethod
    def init_globals(cls):
        from app.tools import tools_list
        from app.utils import setup_model, setup_serp_api, create_workflow

        cls.model = setup_model()
        cls.serp_api = setup_serp_api()
        cls.tool_node = ToolNode(tools_list)
        cls.model = cls.model.bind_tools(tools_list)
        cls.admin_service = init_api(api=DefaultApi, host=os.getenv('ADMIN_SERVICE_HOST'))

        workflow = create_workflow()
        memory = MemorySaver()
        cls.app = workflow.compile(checkpointer=memory)
