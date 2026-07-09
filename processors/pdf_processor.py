from models.processing_result import ProcessingResult
from logger.logger import logger


def process_pdf(content):

    logger.info("📥 PDF Processor: Processing PDF content")

    return ProcessingResult(
        status="success",
        processor="PDF Processor",
        resource_type=content.type,
        message="PDF received."
    )