import pytest
from unittest.mock import MagicMock

from src.pages.inventory_page import InventoryPage


@pytest.fixture
def inv_page():
    drv = MagicMock()
    p = InventoryPage(driver=drv, base_url="https://example.com", default_timeout=5)
    p.wait.until = MagicMock()
    return p


def test_is_loaded_uses_exists(inv_page, monkeypatch):
    called = {"ok": False}

    def fake_exists(*args, **kwargs):
        called["ok"] = True
        return True

    monkeypatch.setattr(inv_page, "exists", fake_exists)
    assert inv_page.is_loaded() is True
    assert called["ok"]


def test_add_first_item_to_cart_clicks_first(inv_page):
    first_btn = MagicMock()
    others = [first_btn, MagicMock()]
    inv_page.driver.find_elements.return_value = others

    inv_page.add_first_item_to_cart()
    first_btn.click.assert_called_once()


def test_add_first_item_to_cart_asserts_when_no_items(inv_page):
    inv_page.driver.find_elements.return_value = []
    with pytest.raises(AssertionError):
        inv_page.add_first_item_to_cart()


def test_cart_count_zero_when_badge_missing(inv_page, monkeypatch):
    monkeypatch.setattr(inv_page, "exists", lambda *a, **k: False)
    assert inv_page.cart_count() == 0


def test_cart_count_returns_int(inv_page, monkeypatch):
    monkeypatch.setattr(inv_page, "exists", lambda *a, **k: True)
    monkeypatch.setattr(inv_page, "text_of", lambda *a, **k: "2")
    assert inv_page.cart_count() == 2
