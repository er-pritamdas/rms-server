"""
Detected Content Models

These models represent the resources that RMS understands after
classifying a ParsedMessage.
"""

from typing import Literal

from pydantic import BaseModel, Field


class DetectedContent(BaseModel):
    """
    Base class for all detected resources.
    """

    type: str
    url: str

    title: str | None = None

    metadata: dict[str, str | int | float | bool] = Field(
        default_factory=dict
    )


# -------------------------------------------------------------------
# Instagram
# -------------------------------------------------------------------


class InstagramReel(DetectedContent):
    type: Literal["instagram_reel"] = "instagram_reel"


class InstagramPost(DetectedContent):
    type: Literal["instagram_post"] = "instagram_post"


class InstagramProfile(DetectedContent):
    type: Literal["instagram_profile"] = "instagram_profile"


# -------------------------------------------------------------------
# YouTube
# -------------------------------------------------------------------


class YoutubeVideo(DetectedContent):
    type: Literal["youtube_video"] = "youtube_video"


class YoutubeShort(DetectedContent):
    type: Literal["youtube_short"] = "youtube_short"


class YoutubePlaylist(DetectedContent):
    type: Literal["youtube_playlist"] = "youtube_playlist"


class YoutubeChannel(DetectedContent):
    type: Literal["youtube_channel"] = "youtube_channel"


# -------------------------------------------------------------------
# GitHub
# -------------------------------------------------------------------


class GithubRepository(DetectedContent):
    type: Literal["github_repository"] = "github_repository"


# -------------------------------------------------------------------
# LinkedIn
# -------------------------------------------------------------------


class LinkedInPost(DetectedContent):
    type: Literal["linkedin_post"] = "linkedin_post"


# -------------------------------------------------------------------
# Documents
# -------------------------------------------------------------------


class PdfDocument(DetectedContent):
    type: Literal["pdf_document"] = "pdf_document"


# -------------------------------------------------------------------
# Generic
# -------------------------------------------------------------------


class Website(DetectedContent):
    type: Literal["website"] = "website"


class UnknownContent(DetectedContent):
    type: Literal["unknown"] = "unknown"