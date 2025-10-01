from __future__ import annotations
import os
import json
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


def _parse_users_from_env() -> dict[str, str]:
    """Parse E2E users from environment variables.

    Priority:
      1. Read `E2E_USERS_JSON` (must be a JSON object). If it is valid and not empty,
         return it as a dict of {username: password}. Keys and values are coerced to str.
      2. Fallback to the demo account composed from:
         - `E2E_DEFAULT_USER` (defaults to "standard_user")
         - `E2E_PASSWORD_standard_user` (defaults to "secret_sauce")

    Returns:
        dict[str, str]: Mapping of usernames to passwords. Guaranteed to be non-empty.
    """
    users_json = os.getenv("E2E_USERS_JSON")
    if users_json:
        try:
            data = json.loads(users_json)
            users = {str(k): str(v) for k, v in data.items()}
            if users:
                return users
        except Exception:
            pass

    default_user = os.getenv("E2E_DEFAULT_USER", "standard_user")
    default_pass = os.getenv("E2E_PASSWORD_standard_user", "secret_sauce")
    return {default_user: default_pass}


@dataclass(frozen=True)
class Settings:
    """Immutable runtime settings sourced from environment variables.

    Attributes:
        base_url: Base URL used by tests (env `BASE_URL`).
        browser: Browser name, e.g. 'chrome' or 'firefox' (env `BROWSER`).
        headless: Run browser in headless mode (env `HEADLESS`).
        default_timeout: Explicit wait timeout in seconds (env `DEFAULT_TIMEOUT`).
        e2e_users: Mapping of usernames to passwords parsed by `_parse_users_from_env`.
        e2e_default_user: The username to be used by default (env `E2E_DEFAULT_USER`).
    """

    base_url: str = os.getenv("BASE_URL", "https://www.saucedemo.com")
    browser: str = os.getenv("BROWSER", "chrome").lower()
    headless: bool = _to_bool(os.getenv("HEADLESS"), False)
    default_timeout: int = int(os.getenv("DEFAULT_TIMEOUT", "10"))

    # Users
    e2e_users: dict[str, str] = None
    e2e_default_user: str = os.getenv("E2E_DEFAULT_USER", "standard_user")

    def __post_init__(self):
        """Finalize settings after dataclass initialization.

        Loads users from environment and ensures `e2e_default_user` exists
        in `e2e_users`. If not present, switches the default to the first
        available user from the mapping.
        """
        object.__setattr__(self, "e2e_users", _parse_users_from_env())

        # If the default user is not in the dictionary, take the first available one
        if self.e2e_default_user not in self.e2e_users:
            first = next(iter(self.e2e_users.keys()))
            object.__setattr__(self, "e2e_default_user", first)


# Singleton settings instance
settings = Settings()
