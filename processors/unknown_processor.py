from models.processing_result import ProcessingResult
from logger.logger import logger


def process_unknown(content):

    logger.warning(f"❓ Unknown Processor: Skipped processing unsupported resource type '{content.type}'")

    return ProcessingResult(
        status="skipped",
        processor="Unknown Processor",
        resource_type=content.type,
        message="Unsupported resource."
    )