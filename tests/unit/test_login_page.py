from unittest.mock import MagicMock
from selenium.webdriver.common.by import By

from src.pages.login_page import LoginPage

TEST_URL = "https://example.com"


def test_open_login_calls_open_root():
    drv = MagicMock()
    page = LoginPage(drv, base_url=TEST_URL, default_timeout=5)

    # Replace .open so as not to touch the driver
    page_open = MagicMock()
    page.open = page_open

    page.open_login()
    page_open.assert_called_once_with("")


def test_login_as_calls_type_and_click():
    drv = MagicMock()
    page = LoginPage(drv, base_url=TEST_URL, default_timeout=5)

    page.type = MagicMock()
    page.click = MagicMock()

    page.login_as("user", "pass")

    # Check that the locators are unpacked correctly
    page.type.assert_any_call(By.ID, "user-name", text="user")
    page.type.assert_any_call(By.ID, "password", text="pass")
    page.click.assert_called_once_with(By.ID, "login-button")


def test_error_message_delegates_to_text_of():
    drv = MagicMock()
    page = LoginPage(drv, base_url=TEST_URL, default_timeout=5)

    page.text_of = MagicMock(return_value="Epic sadface: error")
    assert page.error_message() == "Epic sadface: error"
    page.text_of.assert_called_once_with(By.CSS_SELECTOR, "[data-test='error']")
