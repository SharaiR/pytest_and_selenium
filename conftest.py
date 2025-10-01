from __future__ import annotations
import os
import time
import pathlib
import pytest
from dotenv import load_dotenv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.config import settings
from src.pages.login_page import LoginPage
from src.pages.inventory_page import InventoryPage

# Load .env if present
load_dotenv(override=False)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser", action="store", default=os.getenv("BROWSER", settings.browser)
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=os.getenv("HEADLESS", "false").lower() == "true",
    )
    parser.addoption(
        "--base-url", action="store", default=os.getenv("BASE_URL", settings.base_url)
    )
    parser.addoption("--user", action="store", default=settings.e2e_default_user)


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    return str(pytestconfig.getoption("--base-url"))


@pytest.fixture(scope="session")
def browser_name(pytestconfig: pytest.Config) -> str:
    return str(pytestconfig.getoption("--browser")).lower()


@pytest.fixture(scope="session")
def headless(pytestconfig: pytest.Config) -> bool:
    return bool(pytestconfig.getoption("--headless"))


# Pre-run check: fast pre-check of BASE_URL before any browser spins up
@pytest.fixture(scope="session", autouse=True)
def preruncheck(base_url: str):
    """Fail fast (skip) if the site is unavailable or returns 5xx."""
    if os.getenv("SKIP_PRERUN_CHECK", "false").lower() in {"1", "true", "yes", "y"}:
        return
    try:
        resp = requests.get(base_url, timeout=5)
        if resp.status_code >= 500:
            pytest.skip(
                f"!!! PRE-RUN CHECK: {base_url} responded with {resp.status_code}"
            )
    except Exception as e:
        pytest.skip(f"!!! PRE-RUN CHECK: cannot reach {base_url} — {e}")


@pytest.fixture
def driver(browser_name: str, headless: bool) -> webdriver.Remote:
    # Use Selenium Manager to resolve drivers automatically
    if browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        drv = webdriver.Firefox(options=options)
    else:
        # Default to chrome
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        drv = webdriver.Chrome(options=options)

    drv.implicitly_wait(0)  # rely on explicit waits
    yield drv
    drv.quit()


@pytest.fixture
def pages(driver, base_url):
    class Pages:
        login = LoginPage(driver, base_url)
        inventory = InventoryPage(driver, base_url)

    return Pages()


# Screenshots on failure (pytest-html compatible)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver", None)
        if drv:
            ts = time.strftime("%Y%m%d-%H%M%S")
            safe_name = item.nodeid.replace("::", "_").replace("/", "_")
            out_dir = pathlib.Path("artifacts") / "screenshots"
            out_dir.mkdir(parents=True, exist_ok=True)
            path = out_dir / f"{safe_name}_{ts}.png"
            drv.save_screenshot(str(path))
            # Attach to pytest-html if available
            extra = getattr(item.config, "_html", None)
            if extra is not None:
                from py.xml import html

                rep.extra = getattr(rep, "extra", [])
                rep.extra.append(html.a("screenshot", href=str(path)))


@pytest.fixture(scope="session")
def creds(pytestconfig: pytest.Config):
    user = str(pytestconfig.getoption("--user"))
    users = settings.e2e_users
    if user not in users:
        available = ", ".join(users.keys())
        pytest.exit(f"--user='{user}' not found. Available: {available}")
    return {"user": user, "password": users[user]}


@pytest.fixture
def login(pages, creds):
    pages.login.open_login()
    pages.login.login_as(creds["user"], creds["password"])
    assert pages.inventory.is_loaded(), "Inventory page did not load after login"
    return pages
