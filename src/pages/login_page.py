from __future__ import annotations
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """Page Object for the login page."""
    
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def open_login(self) -> None:
        """Navigate to the login page (root of the site)."""
        self.open("")

    def login_as(self, username: str, password: str) -> None:
        """Perform a login attempt with provided credentials.

        Args:
            username: Account username.
            password: Account password.
        """
        self.type(*self.USERNAME, text=username)
        self.type(*self.PASSWORD, text=password)
        self.click(*self.LOGIN_BTN)

    def error_message(self) -> str:
        """Return the visible error banner text, if any.

        Returns:
            str: Error message text.
        """
        return self.text_of(*self.ERROR)
