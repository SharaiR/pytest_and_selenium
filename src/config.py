from __future__ import annotations
import os
from dataclasses import dataclass


def _to_bool(value: str | None, default: bool) -> bool:
    """Convert common truthy/falsey string values to boolean.

    Accepts '1', 'true', 'yes', 'y', 'on' (case-insensitive) as True.
    If `value` is None, returns `default`.

    Args:
        value: String value from env or None.
        default: Fallback boolean if value is None.

    Returns:
        bool: Parsed boolean.
    """
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    """Immutable runtime settings sourced from environment variables.

    Attributes:
        base_url: Base URL used by tests (env `BASE_URL`).
        browser: Browser name, e.g. 'chrome' or 'firefox' (env `BROWSER`).
        headless: Run browser in headless mode (env `HEADLESS`).
        default_timeout: Explicit wait timeout in seconds (env `DEFAULT_TIMEOUT`).
    """
    base_url: str = os.getenv("BASE_URL", "https://www.saucedemo.com")
    browser: str = os.getenv("BROWSER", "chrome").lower()
    headless: bool = _to_bool(os.getenv("HEADLESS"), False)
    default_timeout: int = int(os.getenv("DEFAULT_TIMEOUT", "10"))


# Singleton settings instance for convenient import in tests/fixtures
settings = Settings()
