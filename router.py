"""
Router

Routes DetectedContent to the correct processor.
"""

from models.detected_content import (
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

from processors.github_processor import process_github
from processors.instagram_processor import process_instagram
from processors.pdf_processor import process_pdf
from processors.unknown_processor import process_unknown
from processors.website_processor import process_website
from processors.youtube_processor import process_youtube


PROCESSOR_REGISTRY = {

    InstagramReel: process_instagram,
    InstagramPost: process_instagram,
    InstagramProfile: process_instagram,

    YoutubeVideo: process_youtube,
    YoutubeShort: process_youtube,
    YoutubePlaylist: process_youtube,
    YoutubeChannel: process_youtube,

    GithubRepository: process_github,

    LinkedInPost: process_website,

    PdfDocument: process_pdf,

    Website: process_website,

    UnknownContent: process_unknown,
}


def route(content):

    processor = PROCESSOR_REGISTRY.get(type(content))

    if processor is None:
        return process_unknown(content)

    return processor(content)