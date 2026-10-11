import logging

import pytest

from knowledgeos.logging_config import configure_logging, get_logger


def test_get_logger_returns_named_standard_logger() -> None:
    assert get_logger("knowledgeos.test").name == "knowledgeos.test"


def test_logging_rejects_unknown_level() -> None:
    with pytest.raises(ValueError, match="Unknown logging level"):
        configure_logging("verbose")


def test_logging_accepts_case_insensitive_level() -> None:
    configure_logging("warning")

    assert logging.getLevelNamesMapping()["WARNING"] == logging.WARNING