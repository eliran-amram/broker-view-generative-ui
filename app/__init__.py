"""
Please DO NOT modify this file !!!
"""
import logging
import uuid
from datetime import datetime, timezone
from functools import partial

from atbay_bootstrap import start_app as start_base_app
from atbay_logger import Logger

from app.errors.handlers import ERROR_HANDLERS
from app.plugins.globals import AppGlobals
from app.prompts import SYSTEM_INSTRUCTIONS
from app.utils import setup_initial_messages, init_agent_for_convos, load_environment_variables


# init
Logger.init_default_logger()
start_app = partial(
    start_base_app, errors_handlers=ERROR_HANDLERS, custom_plugin_location='app/plugins'
)
