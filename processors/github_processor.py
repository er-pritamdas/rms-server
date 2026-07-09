from models.processing_result import ProcessingResult
from logger.logger import logger


def process_github(content):

    logger.info("📥 GitHub Processor: Processing GitHub repository")

    return ProcessingResult(
        status="success",
        processor="GitHub Processor",
        resource_type=content.type,
        message="GitHub repository received."
    )