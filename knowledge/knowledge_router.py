"""
Knowledge Router

Orchestrates the complete Knowledge Extraction Pipeline.
"""

from logger.logger import get_logger

from knowledge.extractors.audio_extractor import run_audio_extraction
from knowledge.models.knowledge import Knowledge
from models.processing_result import ProcessingResult
from knowledge.extractors.frame_extractor import (
    run_frame_extraction,
)
from knowledge.processors.whisper_processor import (
    run_whisper,
)

logger = get_logger(__name__)


def extract_knowledge(
    processing_result: ProcessingResult,
) -> Knowledge:
    """
    Entry point for the Knowledge Extraction Pipeline.

    Current Pipeline
    ----------------
    Processing Result
            ↓
    Initialize Knowledge
            ↓
    Audio Extraction

    Future Pipeline
    ---------------
    Audio Extraction
            ↓
    Whisper
            ↓
    Frame Extraction
            ↓
    OCR
            ↓
    Vision
            ↓
    Knowledge Merger
    """

    logger.info("Starting Knowledge Extraction Pipeline")

    if processing_result.status != "success":
        logger.warning(
            f"Processing result status is not 'success' ({processing_result.status}). Skipping Knowledge Extraction."
        )
        logger.info("Knowledge Extraction Pipeline Complete.")
        return Knowledge(
            resource_id=processing_result.metadata.get("reel_id", ""),
            resource_type=processing_result.resource_type,
        )

    download_path = processing_result.metadata.get("download_path")
    if not download_path:
        logger.info("No download path found in metadata. Skipping Knowledge Extraction.")
        logger.info("Knowledge Extraction Pipeline Complete.")
        return Knowledge(
            resource_id=processing_result.metadata.get("reel_id", ""),
            resource_type=processing_result.resource_type,
        )

    # ==========================================================
    # Initialize Knowledge Object
    # ==========================================================

    knowledge = Knowledge(
        resource_id=processing_result.metadata.get(
            "reel_id",
            "",
        ),
        resource_type=processing_result.resource_type,
    )

    logger.info("Knowledge object initialized.")

    # ==========================================================
    # Audio Extraction
    # ==========================================================

    try:
        logger.info("Running Audio Extractor...")
        knowledge = run_audio_extraction(
            processing_result,
            knowledge,
        )
        logger.info("Audio extraction completed.")
    except Exception as e:
        logger.error(f"Error in Audio Extraction: {str(e)}", exc_info=True)


    # ==========================================================
    # Frame Extraction
    # ==========================================================

    try:
        logger.info("Running Frame Extractor...")
        knowledge = run_frame_extraction(
            processing_result,
            knowledge,
        )
        logger.info("Frame extraction completed.")
    except Exception as e:
        logger.error(f"Error in Frame Extraction: {str(e)}", exc_info=True)


    # ==========================================================
    # Whisper Processor
    # ==========================================================
    try:
        logger.info("Running Whisper Processor...")
        knowledge = run_whisper(
            processing_result,
            knowledge,
        )
        logger.info("Whisper processor completed.")
    except Exception as e:
        logger.error(f"Error in Whisper Processor: {str(e)}", exc_info=True)


    # ==========================================================
    # Future Modules
    # ==========================================================
    #
    #
    # knowledge = run_ocr(
    #     processing_result,
    #     knowledge,
    # )
    #
    # knowledge = run_vision(
    #     processing_result,
    #     knowledge,
    # )
    #
    # knowledge = merge_knowledge(
    #     processing_result,
    #     knowledge,
    # )

    # ==========================================================
    # Complete
    # ==========================================================

    logger.info("Knowledge Extraction Pipeline Complete.")

    logger.info(
        "Knowledge Object : %s",
        knowledge.model_dump(),
    )



    return knowledge