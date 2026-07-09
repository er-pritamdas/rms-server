"""
Whisper Processor

Converts extracted audio into text using Faster Whisper.
"""

import json
from pathlib import Path

from faster_whisper import WhisperModel

from logger.logger import get_logger
from knowledge.models.knowledge import Knowledge
from models.processing_result import ProcessingResult

logger = get_logger(__name__)


# ==========================================================
# Whisper Model
# ==========================================================

# Loaded once when the module is imported.
# Avoids reloading the model for every request.

MODEL = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8",
)


# ==========================================================
# Helpers
# ==========================================================

def transcript_exists(transcript_path: Path) -> bool:
    """
    Check if transcript already exists.
    """

    return transcript_path.exists()


def save_transcript(
    transcript: str,
    transcript_path: Path,
):

    transcript_path.write_text(
        transcript,
        encoding="utf-8",
    )


def save_segments(
    segments,
    json_path: Path,
):

    data = []

    for segment in segments:

        data.append(
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
            }
        )

    with open(
        json_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


# ==========================================================
# Public API
# ==========================================================

def run_whisper(
    processing_result: ProcessingResult,
    knowledge: Knowledge,
) -> Knowledge:
    """
    Generate transcript using Faster Whisper.
    """


    logger.info("Starting Whisper Processor")


    resource_path = Path(
        processing_result.metadata["download_path"]
    )

    extracted_dir = resource_path / "extracted"

    audio_path = extracted_dir / "audio.wav"

    transcript_path = (
        extracted_dir / "transcript.txt"
    )

    transcript_json = (
        extracted_dir / "transcript.json"
    )

    logger.info(
        "Audio Path : %s",
        audio_path,
    )

    # ------------------------------------------------------
    # Validation
    # ------------------------------------------------------

    if not audio_path.exists():

        raise FileNotFoundError(
            f"Audio not found: {audio_path}"
        )

    # ------------------------------------------------------
    # Skip if already exists
    # ------------------------------------------------------

    if transcript_exists(transcript_path):

        logger.info(
            "Transcript already exists. Skipping Whisper."
        )

        transcript = transcript_path.read_text(
            encoding="utf-8"
        )

    else:

        logger.info(
            "Running Faster Whisper..."
        )

        segments, info = MODEL.transcribe(
            str(audio_path),
            beam_size=5,
        )

        segments = list(segments)

        transcript = " ".join(
            segment.text.strip()
            for segment in segments
        )

        save_transcript(
            transcript,
            transcript_path,
        )

        save_segments(
            segments,
            transcript_json,
        )

        logger.info(
            "Language : %s",
            info.language,
        )

        logger.info(
            "Transcript generated successfully."
        )

    # ------------------------------------------------------
    # Update Knowledge
    # ------------------------------------------------------

    knowledge.transcript = transcript

    knowledge.metadata[
        "transcript_path"
    ] = str(transcript_path)

    knowledge.metadata[
        "transcript_json"
    ] = str(transcript_json)

    logger.info(
        "Knowledge updated with transcript."
    )

    logger.info("Whisper Processing Complete")


    return knowledge