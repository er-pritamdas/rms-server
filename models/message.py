"""
Message Models
"""

from pydantic import BaseModel

from models.content import Content


class ParsedMessage(BaseModel):
    """
    Normalized Message Model
    """

    user: str

    channel: str

    timestamp: str

    content: list[Content]