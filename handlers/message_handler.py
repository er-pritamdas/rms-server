"""
Message Handler

Acts as the orchestrator of the RMS application.
"""
from router import route
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

    # print(message)  # Debug print for testing 
    print_message(message)

    # --------------------------------------------------
    # Classify Content
    # --------------------------------------------------

    detected_content = classify_content(message)
    # print(detected_content) # Debug print for testing 

    # --------------------------------------------------
    # Print Classification
    # --------------------------------------------------

    print_detected_content(detected_content)

    # --------------------------------------------------
    # Route to Processor
    # --------------------------------------------------

    for resource in detected_content:
        result = route(resource)
        print(result.model_dump())

    print("✅ Message Processing Complete")
    print("=" * 80)
    print()