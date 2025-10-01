import pytest
from unittest.mock import MagicMock
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from src.pages.base_page import BasePage

TEST_URL = "https://example.com"


@pytest.fixture
def mock_driver():
    drv = MagicMock()
    return drv


@pytest.fixture
def page(mock_driver):
    # base_url without a trailing slash to check normalization
    p = BasePage(driver=mock_driver, base_url=TEST_URL, default_timeout=5)
    # Replace .wait.until so as not to interrupt real EC
    p.wait.until = MagicMock()
    return p


def test_open_builds_correct_url(page, mock_driver):
    page.open("login")
    mock_driver.get.assert_called_once_with(f"{TEST_URL}/login")

    # Check the leading slash
    mock_driver.get.reset_mock()
    page.open("/inventory")
    mock_driver.get.assert_called_once_with(f"{TEST_URL}/inventory")


def test_find_uses_wait_until_presence(page):
    fake_el = MagicMock()
    page.wait.until.return_value = fake_el
    el = page.find(By.ID, "user")
    assert el is fake_el
    page.wait.until.assert_called_once()
    # ensure we passed a locator tuple inside
    args, kwargs = page.wait.until.call_args
    assert callable(args[0])  # expected_conditions возвращает callable


def test_click_waits_until_clickable_and_clicks(page):
    clickable = MagicMock()
    page.wait.until.return_value = clickable
    page.click(By.CSS_SELECTOR, ".btn")
    clickable.click.assert_called_once()


def test_type_clears_then_sends_keys(page):
    visible = MagicMock()
    page.wait.until.return_value = visible
    page.type(By.NAME, "q", "hello", clear=True)
    visible.clear.assert_called_once()
    visible.send_keys.assert_called_once_with("hello")


def test_type_without_clear(page):
    visible = MagicMock()
    page.wait.until.return_value = visible
    page.type(By.NAME, "q", "hello", clear=False)
    visible.clear.assert_not_called()
    visible.send_keys.assert_called_once_with("hello")


def test_text_of_returns_inner_text(page):
    visible = MagicMock()
    visible.text = "Hello"
    page.wait.until.return_value = visible
    assert page.text_of(By.CSS_SELECTOR, ".title") == "Hello"


def test_exists_true(page):
    page.wait.until.return_value = MagicMock()
    assert page.exists(By.ID, "exists") is True


def test_exists_false_on_timeout(page):
    page.wait.until.side_effect = TimeoutException("nope")
    assert page.exists(By.ID, "missing") is False
