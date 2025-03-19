"""
Please DO NOT modify this file !!!
"""
import uvicorn
import asyncio

from fastapi import FastAPI

from app import start_app

app = start_app('fastapi', FastAPI)

async def main(port: int = 8191):
    config = uvicorn.Config(app, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
