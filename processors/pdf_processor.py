from models.processing_result import ProcessingResult


def process_pdf(content):

    print("📥 PDF Processor")

    return ProcessingResult(
        status="success",
        processor="PDF Processor",
        resource_type=content.type,
        message="PDF received."
    )