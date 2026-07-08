"""
Instagram Processor

Responsibilities
----------------
1. Extract Reel ID
2. Create Download Directory
3. Download Reel using yt-dlp
4. Save Metadata
5. Save Caption
6. Return ProcessingResult
"""

import json
import re
from pathlib import Path

from yt_dlp import YoutubeDL

from config import INSTAGRAM_DOWNLOAD_DIR
from models.processing_result import ProcessingResult

# ==========================================================
# Regex
# ==========================================================

REEL_ID_PATTERN = re.compile(
    r"instagram\.com/reels?/([A-Za-z0-9_-]+)"
)


# ==========================================================
# Helper Functions
# ==========================================================

def extract_reel_id(url: str) -> str:
    """
    Extract the Instagram Reel ID.

    Example
    -------
    https://www.instagram.com/reel/DY9Xo30yZNY/

    returns

    DY9Xo30yZNY
    """

    match = REEL_ID_PATTERN.search(url)

    if not match:
        raise ValueError("Invalid Instagram Reel URL.")

    return match.group(1)


def create_download_directory(reel_id: str) -> Path:
    """
    Create download directory.

    downloads/
        instagram/
            <reel_id>/
    """

    download_path = INSTAGRAM_DOWNLOAD_DIR / reel_id

    download_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return download_path


def download_reel(
    url: str,
    download_path: Path,
) -> dict:
    """
    Download Instagram Reel.

    Returns
    -------
    Metadata dictionary returned by yt-dlp.
    """

    ydl_opts = {
        "outtmpl": str(download_path / "reel.%(ext)s"),
        "writethumbnail": True,
        "writeinfojson": False,
        "noplaylist": True,
        "quiet": False,
    }

    with YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=True,
        )

    return info


def save_metadata(
    info: dict,
    download_path: Path,
):
    """
    Save metadata.json
    """

    metadata_file = download_path / "metadata.json"

    with open(
        metadata_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            info,
            file,
            indent=4,
            ensure_ascii=False,
        )


def save_caption(
    info: dict,
    download_path: Path,
):
    """
    Save caption.txt
    """

    caption = (
        info.get("description")
        or info.get("title")
        or ""
    )

    caption_file = download_path / "caption.txt"

    caption_file.write_text(
        caption,
        encoding="utf-8",
    )


def build_processing_result(
    reel_id: str,
    download_path: Path,
) -> ProcessingResult:
    """
    Build ProcessingResult object.
    """

    return ProcessingResult(
        status="success",
        processor="Instagram Processor",
        resource_type="instagram_reel",
        message="Instagram Reel downloaded successfully.",
        metadata={
            "reel_id": reel_id,
            "download_path": str(download_path),
        },
    )


# ==========================================================
# Public API
# ==========================================================

def process_instagram(content):
    """
    Process Instagram Reel.
    """

    try:

        # Step 1
        reel_id = extract_reel_id(content.url)

        # Step 2
        download_path = create_download_directory(reel_id)

        # Step 3
        info = download_reel(
            content.url,
            download_path,
        )

        # Step 4
        save_metadata(
            info,
            download_path,
        )

        # Step 5
        save_caption(
            info,
            download_path,
        )

        # Step 6
        return build_processing_result(
            reel_id,
            download_path,
        )

    except Exception as e:

        return ProcessingResult(
            status="failed",
            processor="Instagram Processor",
            resource_type="instagram_reel",
            message=str(e),
            metadata={},
        )