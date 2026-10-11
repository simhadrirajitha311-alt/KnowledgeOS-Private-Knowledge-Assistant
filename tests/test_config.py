import pytest
from pydantic import ValidationError

from knowledgeos.config import Settings


def test_settings_defaults_are_usable() -> None:
    settings = Settings(_env_file=None)

    assert settings.environment == "local"
    assert settings.chunk_size == 1000
    assert settings.chunk_overlap < settings.chunk_size


def test_settings_read_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KNOWLEDGEOS_CHUNK_SIZE", "800")
    monkeypatch.setenv("KNOWLEDGEOS_CHUNK_OVERLAP", "100")

    settings = Settings(_env_file=None)

    assert settings.chunk_size == 800
    assert settings.chunk_overlap == 100


def test_settings_read_env_file(tmp_path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("KNOWLEDGEOS_RETRIEVAL_TOP_K=9\n")

    settings = Settings(_env_file=env_file)

    assert settings.retrieval_top_k == 9


def test_settings_reject_overlap_equal_to_chunk_size() -> None:
    with pytest.raises(ValidationError, match="chunk_overlap must be smaller"):
        Settings(_env_file=None, chunk_size=500, chunk_overlap=500)


def test_settings_reject_nonpositive_upload_limit() -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, max_upload_size_bytes=0)