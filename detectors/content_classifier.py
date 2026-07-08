"""
Content Classifier

Converts ParsedMessage into detected resources.
"""

import re

from models.content import LinkContent
from models.detected_content import (
    DetectedContent,
    GithubRepository,
    InstagramPost,
    InstagramProfile,
    InstagramReel,
    LinkedInPost,
    PdfDocument,
    UnknownContent,
    Website,
    YoutubeChannel,
    YoutubePlaylist,
    YoutubeShort,
    YoutubeVideo,
)
from models.message import ParsedMessage


# --------------------------------------------------------------------
# URL Patterns
# --------------------------------------------------------------------

INSTAGRAM_REEL = re.compile(r"https?://(www\.)?instagram\.com/reel/")
INSTAGRAM_POST = re.compile(r"https?://(www\.)?instagram\.com/p/")
INSTAGRAM_PROFILE = re.compile(
    r"https?://(www\.)?instagram\.com/[^/?]+/?$"
)

YOUTUBE_SHORT = re.compile(r"https?://(www\.)?youtube\.com/shorts/")
YOUTUBE_VIDEO = re.compile(
    r"https?://(www\.)?(youtube\.com/watch|youtu\.be/)"
)
YOUTUBE_PLAYLIST = re.compile(
    r"https?://(www\.)?youtube\.com/playlist"
)
YOUTUBE_CHANNEL = re.compile(
    r"https?://(www\.)?youtube\.com/@"
)

GITHUB_REPOSITORY = re.compile(
    r"https?://(www\.)?github\.com/[^/]+/[^/]+/?$"
)

LINKEDIN_POST = re.compile(
    r"https?://(www\.)?linkedin\.com/posts/"
)

PDF_DOCUMENT = re.compile(r".*\.pdf($|\?)")


# --------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------


def classify_content(
    message: ParsedMessage,
) -> list[DetectedContent]:
    """
    Classify all links inside a ParsedMessage.
    """

    detected: list[DetectedContent] = []

    for content in message.content:

        if not isinstance(content, LinkContent):
            continue

        detected.append(classify_url(content.value))

    return detected


# --------------------------------------------------------------------
# URL Classification
# --------------------------------------------------------------------


def classify_url(url: str) -> DetectedContent:
    """
    Classify a single URL.
    """

    if INSTAGRAM_REEL.search(url):
        return InstagramReel(url=url)

    if INSTAGRAM_POST.search(url):
        return InstagramPost(url=url)

    if INSTAGRAM_PROFILE.search(url):
        return InstagramProfile(url=url)

    if YOUTUBE_SHORT.search(url):
        return YoutubeShort(url=url)

    if YOUTUBE_VIDEO.search(url):
        return YoutubeVideo(url=url)

    if YOUTUBE_PLAYLIST.search(url):
        return YoutubePlaylist(url=url)

    if YOUTUBE_CHANNEL.search(url):
        return YoutubeChannel(url=url)

    if GITHUB_REPOSITORY.search(url):
        return GithubRepository(url=url)

    if LINKEDIN_POST.search(url):
        return LinkedInPost(url=url)

    if PDF_DOCUMENT.search(url):
        return PdfDocument(url=url)

    if url.startswith(("http://", "https://")):
        return Website(url=url)

    return UnknownContent(url=url)