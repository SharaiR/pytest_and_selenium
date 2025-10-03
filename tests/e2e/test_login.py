import pytest
from src.config import settings


@pytest.mark.e2e
@pytest.mark.smoke
def test_successful_login(pages):
    pages.login.open_login()
    user = settings.e2e_default_user
    password = settings.e2e_users[user]
    pages.login.login_as(user, password)
    assert pages.inventory.is_loaded(), "Inventory page did not load after login"


@pytest.mark.e2e
def test_login_with_wrong_password_shows_error(pages):
    pages.login.open_login()
    user = settings.e2e_default_user
    pages.login.login_as(user, "wrong_password")
    assert "Epic sadface" in pages.login.error_message()
