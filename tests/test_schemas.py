from uuid import uuid4

import pytest
from pydantic import ValidationError

from knowledgeos.schemas import AnswerResponse, DocumentStatus, SearchRequest, SourceReference


def test_search_request_applies_safe_defaults_and_limits() -> None:
    request = SearchRequest(query="Where is the project plan?")

    assert request.top_k == 5
    assert request.document_ids is None
    with pytest.raises(ValidationError):
        SearchRequest(query="", top_k=5)
    with pytest.raises(ValidationError):
        SearchRequest(query="question", top_k=51)


def test_answer_citations_have_stable_source_identifiers() -> None:
    document_id = uuid4()
    chunk_id = uuid4()
    answer = AnswerResponse(
        answer="The plan is in the project notes.",
        sources=[
            SourceReference(
                document_id=document_id,
                chunk_id=chunk_id,
                excerpt="The project plan is in the notes.",
                page_number=2,
            )
        ],
    )

    assert answer.sources[0].document_id == document_id
    assert answer.sources[0].page_number == 2
    assert DocumentStatus.INDEXED == "indexed"


def test_source_reference_rejects_invalid_page_numbers() -> None:
    with pytest.raises(ValidationError):
        SourceReference(
            document_id=uuid4(),
            chunk_id=uuid4(),
            excerpt="A real excerpt.",
            page_number=0,
        )