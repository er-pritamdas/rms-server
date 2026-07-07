"""
Message Handler

Acts as the orchestrator of the application.
"""

from models.message import ParsedMessage
from printers.console_printer import print_message


def handle_message(message: ParsedMessage):
    """
    Process an incoming ParsedMessage.
    """

    print()
    print("=" * 80)
    print("🚀 Processing Message")
    print("=" * 80)

    # Step 1
    print_message(message)

    # Future Steps
    #
    # detect_content(message)
    # download_media(message)
    # transcribe(message)
    # summarize(message)
    # save_to_database(message)

    print("✅ Processing Complete")
    print("=" * 80)
    print()