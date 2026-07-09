"""
Content Models

Every Slack message is converted into one or more Content objects.
"""

from typing import Literal, Optional

from pydantic import BaseModel
from logger.logger import logger

logger.info("Content models module loaded.")


class Content(BaseModel):
    """
    Base Content Model
    """

    type: str


class TextContent(Content):
    """
    Plain Text
    """

    type: Literal["text"] = "text"

    value: str


class EmojiContent(Content):
    """
    Emoji
    """

    type: Literal["emoji"] = "emoji"

    name: str

    unicode: str


class LinkContent(Content):
    """
    Hyperlink
    """

    type: Literal["link"] = "link"

    value: str

    display_text: Optional[str] = None

    truncated: bool = False