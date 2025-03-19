import logging
import os
from pytest import fixture
from time import sleep
logger = logging.getLogger('Integration tests setup')

# # TO GENERATE A NEW RDS INSTANCE FOR TEST SESSION USE THE FOLLOWING CODE ! #

# from automation_utils.aws.aws_resources import AwsResources, AwsServices
# from automation_utils.aws.rds_manager import MySqlDB
# import asyncio

# os.environ['TESTING_MODE'] = 'True'

# @fixture(scope='package')
# def aws_resources() -> AwsResources:
#     aws: AwsResources = AwsResources.start([AwsServices.RDS])
#     yield aws
#     aws.dispose()


# @fixture(scope='package')
# def config_db(aws_resources) -> MySqlDB:
#     db: MySqlDB = aws_resources.get_rds().create_random_aurora_mysql_db()
#     yield db

# import threading
# from atbay_config import Config
# from automation_utils.networking import network_utils
# from app.boot.configuration import setup_config


# @fixture(scope='package')
# def config_app(config_db, mock_server) -> dict:
#     data: dict = {'app_host': '127.0.0.1', 'app_port': network_utils.get_free_tcp_port()}
#     setup_config()
#     config = Config()
#     config.set('SQLALCHEMY_DATABASE_URI', config_db.async_endpoint)
#     return data

# @pytest_asyncio.fixture(scope='function')
# async def setup_database(generate_app, config_db):
#     try:
#         from app.models.db import Base
#         from session_manager_plugin.core.session_maker import create_engine
#     except ModuleNotFoundError:
#         return

#     from atbay_config import Config

#     engine = create_engine(Config())
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# @fixture(scope='package')
# def app(config_app):
#     from web import main as run_fastapi_app
#     thread: threading.Thread = threading.Thread(target=lambda:asyncio.run(run_fastapi_app(config_app.get('app_port'))))
#     thread.daemon = True
#     logger.debug(f'running server at {config_app.get("app_host")}:{config_app.get("app_port")}/api')
#     thread.start()
#     sleep(0.1) # wait for server to start
#     yield app

# @fixture(scope='package')
# def init_all(app, setup_database):
#     pass

# # IF YOU NEED TO CONFIGURE MOCKS WITH MOCK SERVER, USE THE FOLLOWING CODE (THERE ARE MULTIPLE EXAMPLES IN THE AUTOMATION_UTILS TESTS)! #

# from automation_utils.mock_servers.mock_server import MockServer, MockServerClient

# @fixture(scope='package')
# def mock_server() -> MockServer:
#     mockserver = MockServer.getInstance()
#     yield mockserver
#     mockserver.dispose()


# @fixture(scope='function')
# def mock_server_client(mock_server) -> MockServerClient:
#     client = mock_server.client
#     client.reset_all_mappings()
#     yield client

