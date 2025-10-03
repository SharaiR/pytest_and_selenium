import pytest


@pytest.mark.usefixtures("login")
@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.regression
def test_cart_badge_absent_when_empty(pages):
    # On a clean login, the cart should be empty - there should be no badge
    assert pages.inventory.cart_count() in (None, 0), "Expected no badge/0 in cart"


@pytest.mark.usefixtures("login")
@pytest.mark.e2e
@pytest.mark.regression
def test_add_item_to_cart_updates_badge(pages):
    # Add first item
    pages.inventory.add_first_item_to_cart()
    assert pages.inventory.cart_count() == 1, "Cart badge did not update to 1"
