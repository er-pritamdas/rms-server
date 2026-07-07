"""
Slack Message Parser

Converts Slack Events API JSON into our internal ParsedMessage model.
"""

from typing import Optional

from models.content import (
    EmojiContent,
    LinkContent,
    TextContent,
)

from models.message import ParsedMessage


def parse_message(event: dict) -> ParsedMessage:
    """
    Convert a Slack Event into our internal ParsedMessage model.
    """

    parsed_message = ParsedMessage(
        user=event.get("user", ""),
        channel=event.get("channel", ""),
        timestamp=event.get("ts", ""),
        content=[],
    )

    blocks = event.get("blocks", [])

    for block in blocks:

        if block.get("type") != "rich_text":
            continue

        for section in block.get("elements", []):

            if section.get("type") != "rich_text_section":
                continue

            for element in section.get("elements", []):

                parsed_content = parse_element(element)

                if parsed_content is not None:
                    parsed_message.content.append(parsed_content)

    return parsed_message


def parse_element(element: dict):
    """
    Dispatch Slack element to the correct parser.
    """

    element_type = element.get("type")

    parsers = {
        "text": parse_text,
        "emoji": parse_emoji,
        "link": parse_link,
    }

    parser = parsers.get(element_type)

    if parser:
        return parser(element)

    return None


def parse_text(element: dict) -> TextContent:
    """
    Parse Slack text element.
    """

    return TextContent(
        value=element.get("text", ""),
    )


def parse_emoji(element: dict) -> EmojiContent:
    """
    Parse Slack emoji element.
    """

    return EmojiContent(
        name=element.get("name", ""),
        unicode=element.get("unicode", ""),
    )


def parse_link(element: dict) -> LinkContent:
    """
    Parse Slack hyperlink element.
    """

    return LinkContent(
        value=element.get("url", ""),
        display_text=element.get("text"),
        truncated=element.get("truncated", False),
    )