from __future__ import annotations
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base Page Object with explicit waits and common browser helpers.

    Encapsulates navigation, element lookup (presence/visibility), clicking,
    typing and simple text extraction. Designed to be inherited by concrete
    page objects.

    Attributes:
        driver: Selenium WebDriver instance.
        base_url: Base URL used by `open()` for relative paths.
        wait: WebDriverWait configured with `default_timeout`.
    """

    def __init__(
        self, driver: WebDriver, base_url: str, default_timeout: int = 10
    ) -> None:
        """Initialise the page.

        Args:
            driver: Selenium WebDriver.
            base_url: Base URL (e.g. "https://example.com").
            default_timeout: Explicit wait timeout in seconds.
        """
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(self.driver, default_timeout)

    def open(self, path: str = "") -> None:
        """Open a page by appending `path` to the base URL.

        Args:
            path: Relative path like "login" or "/inventory".
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        self.driver.get(url)

    def find(self, by: By, value: str) -> WebElement:
        """Wait for element presence in the DOM and return it.

        Args:
            by: Selenium locator strategy (e.g. By.ID).
            value: Locator value.

        Returns:
            WebElement: The found element (may be invisible).
        """
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_visible(self, by: By, value: str) -> WebElement:
        """Wait for element visibility and return it.

        Args:
            by: Selenium locator strategy.
            value: Locator value.

        Returns:
            WebElement: The visible element.
        """
        return self.wait.until(EC.visibility_of_element_located((by, value)))

    def click(self, by: By, value: str) -> None:
        """Wait until element is clickable and click it.

        Args:
            by: Selenium locator strategy.
            value: Locator value.
        """
        el = self.wait.until(EC.element_to_be_clickable((by, value)))
        el.click()

    def type(self, by: By, value: str, text: str, clear: bool = True) -> None:
        """Type text into a visible element.

        Args:
            by: Selenium locator strategy.
            value: Locator value.
            text: Text to send.
            clear: Whether to clear existing value first.
        """
        el = self.find_visible(by, value)
        if clear:
            el.clear()
        el.send_keys(text)

    def text_of(self, by: By, value: str) -> str:
        """Return the visible text of an element.

        Args:
            by: Selenium locator strategy.
            value: Locator value.

        Returns:
            str: Element text content.
        """
        return self.find_visible(by, value).text

    def exists(self, by: By, value: str) -> bool:
        """Check if element exists (present in DOM).

        Args:
            by: Selenium locator strategy.
            value: Locator value.

        Returns:
            bool: True if element is present within the wait timeout, else False.
        """
        try:
            self.find(by, value)
            return True
        except Exception:
            return False
