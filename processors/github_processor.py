from models.processing_result import ProcessingResult


def process_github(content):

    print("📥 GitHub Processor")

    return ProcessingResult(
        status="success",
        processor="GitHub Processor",
        resource_type=content.type,
        message="GitHub repository received."
    )