"""
Processing Result Model
"""

from typing import Literal

from pydantic import BaseModel, Field
from logger.logger import logger

logger.info("Processing result models module loaded.")


class ProcessingResult(BaseModel):
    """
    Standard response returned by every processor.
    """

    status: Literal["success", "failed", "skipped"]

    processor: str

    resource_type: str

    message: str

    metadata: dict = Field(default_factory=dict)