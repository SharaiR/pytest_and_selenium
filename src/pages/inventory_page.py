from __future__ import annotations
from selenium.webdriver.common.by import By
from .base_page import BasePage


class InventoryPage(BasePage):
    """Page Object for the inventory (product listing) page."""
    
    TITLE = (By.CSS_SELECTOR, ".title")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")
    CART_BADGE = (By.CSS_SELECTOR, ".shopping_cart_badge")

    def is_loaded(self) -> bool:
        """Return True if the inventory page appears to be loaded."""
        return self.exists(*self.TITLE)

    def add_first_item_to_cart(self) -> None:
        """Add the first visible item to the shopping cart.

        Raises:
            AssertionError: If no inventory items are found.
        """
        btns = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        assert btns, "No inventory items found"
        btns[0].click()

    def cart_count(self) -> int:
        """Return the numeric badge value of items in the cart.

        Returns:
            int: Count shown in the cart badge, or 0 if the badge is absent.
        """
        if not self.exists(*self.CART_BADGE):
            return 0
        return int(self.text_of(*self.CART_BADGE))
