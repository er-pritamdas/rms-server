"""
Message Handler

Acts as the orchestrator of the RMS application.
"""

from detectors.content_classifier import classify_content
from models.message import ParsedMessage
from printers.console_printer import (
    print_detected_content,
    print_message,
)


def handle_message(message: ParsedMessage):
    """
    Process an incoming ParsedMessage.
    """

    print()
    print("=" * 80)
    print("🚀 Processing Incoming Message")
    print("=" * 80)

    # --------------------------------------------------
    # Print Parsed Message
    # --------------------------------------------------

    print_message(message)

    # --------------------------------------------------
    # Classify Content
    # --------------------------------------------------

    detected_content = classify_content(message)

    # --------------------------------------------------
    # Print Classification
    # --------------------------------------------------

    print_detected_content(detected_content)

    print("✅ Message Processing Complete")
    print("=" * 80)
    print()