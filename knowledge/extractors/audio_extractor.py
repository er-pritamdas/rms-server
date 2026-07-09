"""
Audio Extractor

Extracts WAV audio from downloaded video resources.
"""

from pathlib import Path

from logger.logger import get_logger

from knowledge.models.knowledge import Knowledge
from knowledge.utils.media_utils import (
    audio_exists,
    extract_audio,
    video_exists,
)
from models.processing_result import ProcessingResult

logger = get_logger(__name__)


# ==========================================================
# Public API
# ==========================================================

def run_audio_extraction(
    processing_result: ProcessingResult,
    knowledge: Knowledge,
) -> Knowledge:
    """
    Extract audio from a downloaded video.

    Parameters
    ----------
    processing_result
        Result returned by the resource processor.

    knowledge
        Knowledge object being enriched.

    Returns
    -------
    Updated Knowledge object.
    """

    logger.info("Starting Audio Extraction")

    resource_path = Path(
        processing_result.metadata["download_path"]
    )

    source_dir = resource_path / "source"

    extracted_dir = resource_path / "extracted"

    extracted_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    video_path = source_dir / "reel.mp4"
    if not video_path.exists():
        video_path = resource_path / "reel.mp4"

    audio_path = extracted_dir / "audio.wav"

    logger.info("Video Path : %s", video_path)
    logger.info("Audio Path : %s", audio_path)

    # ------------------------------------------------------
    # Validation
    # ------------------------------------------------------

    if not video_exists(video_path):

        raise FileNotFoundError(
            f"Video not found: {video_path}"
        )

    # ------------------------------------------------------
    # Idempotency
    # ------------------------------------------------------

    if audio_exists(audio_path):

        logger.info(
            "Audio already exists. Skipping extraction."
        )

    else:

        logger.info("Extracting audio...")

        extract_audio(
            video_path,
            audio_path,
        )

        logger.info("Audio extracted successfully.")

    # ------------------------------------------------------
    # Update Knowledge
    # ------------------------------------------------------

    knowledge.metadata["audio_path"] = str(audio_path)

    logger.info(
        "Knowledge updated with audio path."
    )

    logger.info("Audio Extraction Complete")

    return knowledge