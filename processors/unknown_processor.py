from models.processing_result import ProcessingResult


def process_unknown(content):

    print("❓ Unknown Processor")

    return ProcessingResult(
        status="skipped",
        processor="Unknown Processor",
        resource_type=content.type,
        message="Unsupported resource."
    )