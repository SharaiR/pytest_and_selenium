import json
import pytest
from src.config import Settings, _parse_users_from_env

# Helper: clearing environment variables that affect parsing
ENV_KEYS = ["E2E_USERS_JSON", "E2E_DEFAULT_USER", "E2E_PASSWORD_standard_user"]


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    # Before each test, we remove environment variables to avoid session influence
    for k in ENV_KEYS:
        monkeypatch.delenv(k, raising=False)


def test_returns_json_mapping_when_valid_json(monkeypatch):
    data = {"standard_user": "secret_sauce", "problem_user": "pwd2"}
    monkeypatch.setenv("E2E_USERS_JSON", json.dumps(data))

    users = _parse_users_from_env()

    assert users == {"standard_user": "secret_sauce", "problem_user": "pwd2"}
    assert all(isinstance(k, str) and isinstance(v, str) for k, v in users.items())


def test_casts_non_string_values_to_string(monkeypatch):
    data = {"u1": 123, 42: True}
    monkeypatch.setenv("E2E_USERS_JSON", json.dumps(data))

    users = _parse_users_from_env()

    assert users == {"u1": "123", "42": "True"}


def test_fallback_when_json_is_missing(monkeypatch):
    # JSON is not specified, use default from env (if any) or hardcoded defaults
    monkeypatch.setenv("E2E_DEFAULT_USER", "demo")
    monkeypatch.setenv("E2E_PASSWORD_standard_user", "demo_pass")

    users = _parse_users_from_env()

    assert users == {"demo": "demo_pass"}


def test_fallback_when_json_is_empty_object(monkeypatch):
    monkeypatch.setenv("E2E_USERS_JSON", "{}")
    monkeypatch.setenv("E2E_DEFAULT_USER", "demo2")
    monkeypatch.setenv("E2E_PASSWORD_standard_user", "demo2_pass")

    users = _parse_users_from_env()

    assert users == {"demo2": "demo2_pass"}


def test_fallback_when_json_is_invalid(monkeypatch):
    # Invalid JSON - fallback
    monkeypatch.setenv("E2E_USERS_JSON", "{not-a-json}")
    monkeypatch.setenv("E2E_DEFAULT_USER", "demo3")
    monkeypatch.setenv("E2E_PASSWORD_standard_user", "demo3_pass")

    users = _parse_users_from_env()

    assert users == {"demo3": "demo3_pass"}


def test_defaults_when_nothing_set(monkeypatch):
    users = _parse_users_from_env()

    assert users == {"standard_user": "secret_sauce"}


def test_post_init_keeps_existing_default_user(monkeypatch):
    data = {"standard_user": "secret_sauce", "problem_user": "pwd"}
    monkeypatch.setenv("E2E_USERS_JSON", json.dumps(data))

    settings = Settings(e2e_users={"should": "be replaced"}, e2e_default_user="standard_user")

    assert settings.e2e_users == data
    assert settings.e2e_default_user == "standard_user"


def test_post_init_switches_default_when_missing(monkeypatch):
    data = {"first_user": "first_pwd", "second_user": "second_pwd"}
    monkeypatch.setenv("E2E_USERS_JSON", json.dumps(data))

    settings = Settings(e2e_users={"should": "be replaced"}, e2e_default_user="ghost")

    assert settings.e2e_users == data
    assert settings.e2e_default_user == "first_user"
