import json
import logging
import uuid
from typing import Dict, Any
from fastapi import APIRouter, Request
from langchain_core.messages import HumanMessage, AIMessage
from app.plugins.globals import AppGlobals


router = APIRouter(prefix="/bot")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_conversation(user_input: str, config: Dict[str, Any]):
    last_msg = {}
    user_message = HumanMessage(content=user_input)

    for event in AppGlobals.app.stream({"messages": [user_message]}, config, stream_mode="values"):
        if type(event["messages"][-1]) != AIMessage:
            continue
        else:
            last_msg = event["messages"][-1]

    print(f'{last_msg.content}')
    return json.loads(last_msg.content)


@router.post('/chat', operation_id='chat_with_bot', response_model_exclude_unset=True)
async def chat_with_bot(request: Request):
    payload = await request.json()

    chat_id = payload.get('chat_id', str(uuid.uuid4()))
    logging.info(f"Chat ID: {chat_id}")
    config = {"configurable": {"thread_id": 1}}  # TODO: this should be legit id

    return run_conversation(payload.get('message'), config)
