"""
Please DO NOT modify this file !!!
"""
import yaml
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app import start_app
import os


def export_openapi_yaml(service_name: str, version: str, yaml_file: str = 'api.yaml'):
    os.environ.update({'APP_NAME': '', 'ENV': '', 'TESTING_MODE': 'True'})
    api_app = start_app('openapi_exporter', FastAPI)
    with open(yaml_file, 'w') as file:
        file.write(
            yaml.dump(
                get_openapi(title=service_name, version=version, routes=api_app.routes),
                sort_keys=False,
            )
        )
