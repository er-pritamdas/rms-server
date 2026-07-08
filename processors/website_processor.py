from models.processing_result import ProcessingResult


def process_website(content):

    print("🌐 Website Processor")

    return ProcessingResult(
        status="success",
        processor="Website Processor",
        resource_type=content.type,
        message="Website received."
    )