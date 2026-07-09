"""
Knowledge Model

Represents the final structured knowledge extracted from a resource.
"""

from pydantic import BaseModel, Field
from logger.logger import logger

logger.info("Knowledge model module loaded.")


class Knowledge(BaseModel):
    """
    Canonical Knowledge Object.

    Every extractor contributes towards building this object.
    """

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    resource_id: str
    resource_type: str

    # --------------------------------------------------
    # Core Knowledge
    # --------------------------------------------------

    title: str | None = None

    summary: str | None = None

    transcript: str | None = None

    extracted_text: str | None = None

    vision_description: str | None = None

    # --------------------------------------------------
    # AI
    # --------------------------------------------------

    tags: list[str] = Field(default_factory=list)

    entities: list[str] = Field(default_factory=list)

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict = Field(default_factory=dict)