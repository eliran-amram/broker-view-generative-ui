"""
Please DO NOT modify this file !!!
"""
from functools import partial
from app import start_app


def init_typer():
    from typer import Typer
    return Typer()


app = start_app('typer', init_typer)


if __name__ == "__main__":
    app()
