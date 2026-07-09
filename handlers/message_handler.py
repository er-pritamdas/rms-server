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
from knowledge.knowledge_router import extract_knowledge
from logger.logger import logger


def handle_message(message: ParsedMessage):
    """
    Process an incoming ParsedMessage.
    """

    logger.info(
        f"Processing incoming message from user '{message.user}' in channel '{message.channel}'"
    )
    logger.info(f"Parsed message details: {message.model_dump()}")

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

    logger.info("Classifying message content...")
    detected_content = classify_content(message)
    logger.info(
        f"Classified content successfully. Detected {len(detected_content)} resources."
    )

    # --------------------------------------------------
    # Print Classification
    # --------------------------------------------------

    print_detected_content(detected_content)

    # --------------------------------------------------
    # Route to Processor
    # --------------------------------------------------

    for resource in detected_content:
        logger.info(f"Routing resource type '{resource.type}' to appropriate processor...")
        result = route(resource)
        logger.info(
            f"Processor result: status={result.status}, processor={result.processor}, message={result.message}"
        )
        knowledge = extract_knowledge(result)
        logger.info(f"Knowledge Object Created: {knowledge.model_dump()}")
        logger.info(f"Processor result details: {result.model_dump()}")
        print(result.model_dump())

    logger.info("Incoming message processing complete.")
    print("✅ Message Processing Complete")
    print("=" * 80)
    print()