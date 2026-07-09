"""
Media Utilities

Low-level media operations using FFmpeg.
"""

import shutil
import subprocess
from pathlib import Path

from logger.logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# Validation
# ==========================================================

def check_ffmpeg() -> bool:
    """
    Check whether FFmpeg is installed.
    """
    try:
        import imageio_ffmpeg
        imageio_ffmpeg.get_ffmpeg_exe()
        return True
    except (ImportError, RuntimeError):
        pass

    return shutil.which("ffmpeg") is not None


def get_ffmpeg_binary() -> str:
    """
    Get the path to the FFmpeg binary.
    """
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except (ImportError, RuntimeError):
        pass
    return "ffmpeg"



def video_exists(video_path: Path) -> bool:
    """
    Check if video file exists.
    """

    return video_path.exists()


def audio_exists(audio_path: Path) -> bool:
    """
    Check if extracted audio already exists.
    """

    return audio_path.exists()


def frames_exist(frames_dir: Path) -> bool:
    """
    Check if frame directory contains extracted frames.
    """

    if not frames_dir.exists():
        return False

    return any(frames_dir.glob("frame_*.jpg"))


# ==========================================================
# Internal Helper
# ==========================================================

def run_ffmpeg(command: list[str]) -> None:
    """
    Execute an FFmpeg command.
    """

    if not check_ffmpeg():
        raise RuntimeError(
            "FFmpeg is not installed or not found in PATH."
        )

    binary = get_ffmpeg_binary()
    if command and command[0] == "ffmpeg":
        command[0] = binary

    logger.info("Running FFmpeg command:")
    logger.info(" ".join(command))

    subprocess.run(
        command,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


# ==========================================================
# Audio Extraction
# ==========================================================

def extract_audio(
    video_path: Path,
    output_audio: Path,
) -> Path:
    """
    Extract mono 16kHz WAV audio from a video.

    Returns
    -------
    Path to the generated WAV file.
    """

    logger.info("Extracting audio from video...")

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(output_audio),
    ]

    run_ffmpeg(command)

    logger.info(
        "Audio extraction complete: %s",
        output_audio,
    )

    return output_audio


# ==========================================================
# Frame Extraction
# ==========================================================

def extract_frames(
    video_path: Path,
    frames_dir: Path,
    fps: float = 1.0,
) -> Path:
    """
    Extract frames from a video.

    Parameters
    ----------
    fps
        Frames extracted per second.
        Default = 1 frame/sec.
    """

    logger.info("Extracting video frames...")

    frames_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_pattern = frames_dir / "frame_%04d.jpg"

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vf",
        f"fps={fps}",
        str(output_pattern),
    ]

    run_ffmpeg(command)

    logger.info(
        "Frame extraction complete: %s",
        frames_dir,
    )

    return frames_dir