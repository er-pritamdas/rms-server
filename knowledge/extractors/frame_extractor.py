"""
Frame Extractor

Extracts image frames from downloaded video resources.
"""

from pathlib import Path

from logger.logger import get_logger

from knowledge.models.knowledge import Knowledge
from knowledge.utils.media_utils import (
    extract_frames,
    frames_exist,
    video_exists,
)
from models.processing_result import ProcessingResult

logger = get_logger(__name__)


# ==========================================================
# Public API
# ==========================================================

def run_frame_extraction(
    processing_result: ProcessingResult,
    knowledge: Knowledge,
) -> Knowledge:
    """
    Extract frames from a downloaded video.

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

    logger.info("Starting Frame Extraction")

    resource_path = Path(
        processing_result.metadata["download_path"]
    )

    source_dir = resource_path / "source"

    frames_dir = resource_path / "frames"

    frames_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    video_path = source_dir / "reel.mp4"
    if not video_path.exists():
        video_path = resource_path / "reel.mp4"

    logger.info("Video Path : %s", video_path)
    logger.info("Frames Dir : %s", frames_dir)

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

    if frames_exist(frames_dir):

        logger.info(
            "Frames already exist. Skipping extraction."
        )

    else:

        logger.info("Extracting frames...")

        extract_frames(
            video_path,
            frames_dir,
            fps=1.0,
        )

        logger.info("Frames extracted successfully.")

    # ------------------------------------------------------
    # Count extracted frames
    # ------------------------------------------------------

    frame_count = len(
        list(
            frames_dir.glob("frame_*.jpg")
        )
    )

    logger.info(
        "Total Frames : %d",
        frame_count,
    )

    # ------------------------------------------------------
    # Update Knowledge
    # ------------------------------------------------------

    knowledge.metadata["frames_path"] = str(frames_dir)

    knowledge.metadata["frame_count"] = frame_count

    logger.info(
        "Knowledge updated with frame information."
    )

    logger.info("Frame Extraction Complete")

    return knowledge