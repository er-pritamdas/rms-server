from models.processing_result import ProcessingResult
from logger.logger import logger


def process_website(content):

    logger.info(f"🌐 Website Processor: Processing website URL {content.url}")

    return ProcessingResult(
        status="success",
        processor="Website Processor",
        resource_type=content.type,
        message="Website received."
    )