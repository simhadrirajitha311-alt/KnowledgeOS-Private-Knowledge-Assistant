"""Validated data contracts used at KnowledgeOS application boundaries."""

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DocumentStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    INDEXED = "indexed"
    FAILED = "failed"


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=4000)
    document_ids: list[UUID] | None = None
    top_k: int = Field(default=5, ge=1, le=50)


class SourceReference(BaseModel):
    document_id: UUID
    chunk_id: UUID
    excerpt: str = Field(min_length=1)
    page_number: int | None = Field(default=None, ge=1)


class AnswerResponse(BaseModel):
    answer: str
    sources: list[SourceReference] = Field(default_factory=list)
    insufficient_evidence: bool = False
    warnings: list[str] = Field(default_factory=list)


class DocumentSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    filename: str = Field(min_length=1)
    media_type: str
    size_bytes: int = Field(ge=0)
    status: DocumentStatus
    created_at: datetime