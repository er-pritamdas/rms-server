"""
Processing Result Model
"""

from typing import Literal

from pydantic import BaseModel, Field


class ProcessingResult(BaseModel):
    """
    Standard response returned by every processor.
    """

    status: Literal["success", "failed", "skipped"]

    processor: str

    resource_type: str

    message: str

    metadata: dict = Field(default_factory=dict)