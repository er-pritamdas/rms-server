"""
Message Models
"""

from pydantic import BaseModel
from logger.logger import logger

logger.info("Message models module loaded.")

from models.content import Content


class ParsedMessage(BaseModel):
    """
    Normalized Message Model
    """

    user: str

    channel: str

    timestamp: str

    content: list[Content]