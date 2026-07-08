from models.processing_result import ProcessingResult


def process_youtube(content):

    print("📥 YouTube Processor")

    return ProcessingResult(
        status="success",
        processor="YouTube Processor",
        resource_type=content.type,
        message="YouTube content received."
    )