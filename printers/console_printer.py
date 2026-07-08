"""
Console Printer

Pretty prints ParsedMessage and DetectedContent objects.
"""

from models.content import (
    Content,
    EmojiContent,
    LinkContent,
    TextContent,
)

from models.detected_content import DetectedContent
from models.message import ParsedMessage


# ==========================================================
# Parsed Message
# ==========================================================


def print_message(message: ParsedMessage):

    print()

    print("📩 Parsed Message")
    print("-" * 80)

    print(f"👤 User      : {message.user}")
    print(f"📺 Channel   : {message.channel}")
    print(f"⏰ Timestamp : {message.timestamp}")

    print()

    print("Content")
    print("-" * 80)

    if not message.content:
        print("No Content Found")

    for content in message.content:
        print_content(content)

    print()


# ==========================================================
# Content
# ==========================================================


def print_content(content: Content):

    if isinstance(content, TextContent):
        print_text(content)

    elif isinstance(content, EmojiContent):
        print_emoji(content)

    elif isinstance(content, LinkContent):
        print_link(content)

    else:
        print_unknown(content)


def print_text(content: TextContent):

    print("📝 Text")
    print(f"    {content.value}")
    print()


def print_emoji(content: EmojiContent):

    print("😊 Emoji")
    print(f"    Name     : {content.name}")
    print(f"    Unicode  : U+{content.unicode.upper()}")
    print()


def print_link(content: LinkContent):

    print("🔗 Link")
    print(f"    URL           : {content.value}")

    if content.display_text:
        print(f"    Display Text  : {content.display_text}")

    print()


def print_unknown(content: Content):

    print("❓ Unknown Content")
    print(content.model_dump())
    print()


# ==========================================================
# Detected Content
# ==========================================================


def print_detected_content(
    detected_content: list[DetectedContent],
):

    print()
    print("🔍 Content Classification")
    print("-" * 80)

    if not detected_content:
        print("No resources detected.")
        print()
        return

    for resource in detected_content:

        print(f"✅ {resource.type}")

        print(f"    URL : {resource.url}")

        if resource.title:
            print(f"    Title : {resource.title}")

        if resource.metadata:

            print("    Metadata")

            for key, value in resource.metadata.items():
                print(f"        {key}: {value}")

        print()

    print("-" * 80)
    print()