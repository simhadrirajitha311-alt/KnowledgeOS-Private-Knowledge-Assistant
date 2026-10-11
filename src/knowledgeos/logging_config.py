"""Small, dependency-free logging configuration for local development."""

import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure standard-library logging using a validated level name."""

    normalized_level = level.upper()
    numeric_level = logging.getLevelNamesMapping().get(normalized_level)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Unknown logging level: {level}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )


def get_logger(name: str) -> logging.Logger:
    """Return a named logger for a module or application component."""

    return logging.getLogger(name)