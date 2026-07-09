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
from logger.logger import logger

# ==========================================================
# Regex
# ==========================================================

REEL_ID_PATTERN = re.compile(
    r"instagram\.com/(?:reels?|p)/([A-Za-z0-9_-]+)"
)


# ==========================================================
# Helper Functions
# ==========================================================

def extract_reel_id(url: str) -> str:
    """
    Extract the Instagram Reel or Post ID.

    Example
    -------
    https://www.instagram.com/reel/DY9Xo30yZNY/
    https://www.instagram.com/p/DXT8xjyjYPR/

    returns

    DY9Xo30yZNY or DXT8xjyjYPR
    """

    match = REEL_ID_PATTERN.search(url)

    if not match:
        if "instagram.com/" in url and not any(x in url for x in ["/reel/", "/reels/", "/p/"]):
            raise ValueError("Instagram profiles are not supported.")
        raise ValueError("Invalid Instagram Reel or Post URL.")

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
    resource_type: str = "instagram_reel",
) -> ProcessingResult:
    """
    Build ProcessingResult object.
    """

    media_type_name = "Reel" if "reel" in resource_type else "Post"
    return ProcessingResult(
        status="success",
        processor="Instagram Processor",
        resource_type=resource_type,
        message=f"Instagram {media_type_name} downloaded successfully.",
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
    Process Instagram Reel or Post.
    """

    try:
        logger.info(f"Processing Instagram content URL: {content.url}")

        # Step 1
        logger.info("Step 1: Extracting Reel/Post ID...")
        reel_id = extract_reel_id(content.url)
        logger.info(f"Extracted ID: {reel_id}")

        # Step 2
        logger.info("Step 2: Creating download directory...")
        download_path = create_download_directory(reel_id)
        logger.info(f"Download directory path: {download_path}")

        # Step 3
        logger.info(f"Step 3: Downloading from {content.url}...")
        info = download_reel(
            content.url,
            download_path,
        )
        logger.info(f"Content downloaded successfully to: {download_path}")

        # Step 4
        logger.info("Step 4: Saving metadata...")
        save_metadata(
            info,
            download_path,
        )
        logger.info(f"Metadata saved successfully to: {download_path / 'metadata.json'}")

        # Step 5
        logger.info("Step 5: Saving caption...")
        save_caption(
            info,
            download_path,
        )
        logger.info(f"Caption saved successfully to: {download_path / 'caption.txt'}")

        # Step 6
        logger.info("Step 6: Building processing result...")
        result = build_processing_result(
            reel_id,
            download_path,
            resource_type=content.type,
        )
        logger.info(f"Instagram processing result built: {result.model_dump()}")
        return result

    except Exception as e:
        logger.error(f"Error occurred in Instagram processor: {str(e)}", exc_info=True)

        return ProcessingResult(
            status="failed",
            processor="Instagram Processor",
            resource_type=getattr(content, "type", "instagram_reel"),
            message=str(e),
            metadata={},
        )