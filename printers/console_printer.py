"""
Console Printer

Pretty prints ParsedMessage objects.
"""

from models.content import (
    Content,
    EmojiContent,
    LinkContent,
    TextContent,
)

from models.message import ParsedMessage


def print_message(message: ParsedMessage):
    """
    Pretty print a ParsedMessage.
    """

    print()

    print("=" * 80)
    print("📩 New Slack Message")
    print("=" * 80)

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

    print("=" * 80)
    print()


def print_content(content: Content):
    """
    Dispatch content to the correct printer.
    """

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

    print(f"    URL          : {content.value}")

    if content.display_text:
        print(f"    Display Text : {content.display_text}")

    print(f"    Truncated    : {content.truncated}")

    print()


def print_unknown(content: Content):

    print("❓ Unknown Content")

    print(content.model_dump())

    print()