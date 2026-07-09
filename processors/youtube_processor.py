from models.processing_result import ProcessingResult
from logger.logger import logger


def process_youtube(content):

    logger.info(f"📥 YouTube Processor: Processing YouTube resource type '{content.type}'")

    return ProcessingResult(
        status="success",
        processor="YouTube Processor",
        resource_type=content.type,
        message="YouTube content received."
    )