"""
Please DO NOT modify this file !!!
"""
from functools import partial

from atbay_bootstrap import start_app as start_base_app
from atbay_logger import Logger

from app.errors.handlers import ERROR_HANDLERS

Logger.init_default_logger()
start_app = partial(
    start_base_app, errors_handlers=ERROR_HANDLERS, custom_plugin_location='app/plugins'
)