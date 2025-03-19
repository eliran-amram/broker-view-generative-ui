"""
Please DO NOT modify this file !!!
"""
import logging

from fastapi import APIRouter

router = APIRouter(prefix='/health_check')
logger = logging.getLogger(__name__)


@router.get('')
async def health_check():
    return {'healthy': True}
