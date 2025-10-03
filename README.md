# pytest-selenium-template
[![CI](https://github.com/SharaiR/pytest_and_selenium/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/SharaiR/pytest_and_selenium/actions/workflows/ci.yml)
[![pages-build-deployment](https://github.com/SharaiR/pytest_and_selenium/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/SharaiR/pytest_and_selenium/actions/workflows/pages/pages-build-deployment)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/pypi/v/selenium.svg?label=selenium)](https://pypi.org/project/selenium/)
[![pytest](https://img.shields.io/badge/tested_with-pytest-green.svg)](https://docs.pytest.org/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/)
[![flake8](https://img.shields.io/badge/lint-flake8-lightgrey.svg)](https://flake8.pycqa.org/)
![parallel](https://img.shields.io/badge/parallel-pytest--xdist-yellowgreen)
![coverage](https://img.shields.io/endpoint?url=https://sharair.github.io/pytest_and_selenium/coverage.json)
[![Allure](https://img.shields.io/badge/report-Allure-ff69b4)](https://sharair.github.io/pytest_and_selenium/)

A production-ready **Pytest + Selenium** template featuring the Page Object Model, reusable fixtures, fast local execution, and rich reporting. The project is tuned for both browser-driven E2E regression tests and fast unit checks of helper utilities.

---

## Table of contents
- [pytest-selenium-template](#pytest-selenium-template)
  - [Table of contents](#table-of-contents)
  - [Why this template](#why-this-template)
  - [Feature highlights](#feature-highlights)
  - [Tech stack](#tech-stack)
  - [Prerequisites](#prerequisites)
  - [Quick start](#quick-start)
  - [Configuration](#configuration)
  - [Running the tests](#running-the-tests)
  - [Reports \& artifacts](#reports--artifacts)
  - [Continuous integration](#continuous-integration)
  - [Project structure](#project-structure)
  - [Troubleshooting](#troubleshooting)
  - [License](#license)

---

## Why this template
- Opinionated defaults for UI automation that still remain easy to change.
- Deterministic fixture design: each test gets its own WebDriver instance and environment-aware credentials.
- Unit tests cover low-level helpers (e.g., config parsing) to keep feedback fast.
- CI-ready from day one, including Allure publishing and a live coverage badge.

---

## Feature highlights
- ✅ Page Object Model with explicit waits and concise actions.
- ✅ Environment-driven credentials via a frozen `Settings` dataclass.
- ✅ Automatic WebDriver management through Selenium Manager.
- ✅ Screenshots on failure wired into `pytest-html`.
- ✅ Parallel execution using `pytest-xdist`.
- ✅ HTML, Allure, and coverage reporting (locally and in CI).
- ✅ Pre-run health checks that skip tests if the target site is down.
- ✅ Linting/formatting with `flake8` and `black` plus coverage gates.

---

## Tech stack
- **Python** 3.13+
- **Selenium 4** with Chrome or Firefox (WebDriver Manager built-in)
- **pytest** with markers, fixtures, and `pytest-html`
- **pytest-xdist** for parallelism
- **Allure** for interactive dashboards (optional local viewer)
- **Requests** for pre-run availability checks

---

## Prerequisites
- Python 3.13 or newer
- Google Chrome or Mozilla Firefox installed locally (Selenium Manager will fetch drivers automatically)
- `pip` and `venv` (or an equivalent environment manager)
- Optional: [Allure Commandline](https://docs.qameta.io/allure/) for local report viewing
- Optional: `make` if you prefer makefile-based shortcuts (not required)

---

## Quick start
```bash
# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy the example environment file and adjust as needed
cp .env.example .env

# Run a basic smoke suite in headless Chrome
pytest -m "smoke" --browser=chrome --headless
```

> The fixtures in `conftest.py` automatically load `.env` variables via `python-dotenv`.

---

## Configuration
Runtime configuration is controlled by environment variables that feed the immutable `Settings` dataclass in `src/config.py`.

| Variable | Description | Default |
| --- | --- | --- |
| `BASE_URL` | Target application URL | `https://www.saucedemo.com` |
| `BROWSER` | `chrome` or `firefox` | `chrome` |
| `HEADLESS` | `true/false` (case-insensitive) | `false` |
| `DEFAULT_TIMEOUT` | Explicit wait timeout in seconds | `10` |
| `E2E_DEFAULT_USER` | Username used by default | `standard_user` |
| `E2E_PASSWORD_standard_user` | Password for default user | `secret_sauce` |
| `E2E_USERS_JSON` | JSON object mapping usernames to passwords | fallback user map |

> ℹ️ Do not add real user data and passwords to the documentation, only test data.

Example `.env`:
```ini
BASE_URL=https://www.saucedemo.com
BROWSER=chrome
HEADLESS=true
E2E_DEFAULT_USER=standard_user
E2E_PASSWORD_standard_user=secret_sauce
E2E_USERS_JSON={"standard_user": "secret_sauce", "problem_user": "secret_sauce"}
```

Command-line overrides (via `pytest_addoption`) are available for `--browser`, `--headless`, `--base-url`, and `--user`.

---

## Running the tests
```bash
# Unit tests with coverage (term + HTML output)
pytest tests/unit --cov=src --cov-report=term-missing
coverage html -d reports/coverage

# Smoke E2E run (headless Chrome + HTML report)
pytest -m "smoke" --browser=chrome --headless \
  --html=reports/report.html --self-contained-html

# Full UI regression and Allure results
pytest -m "e2e or regression" --browser=chrome --headless \
  --alluredir=reports/allure-results

# Parallel execution (auto-detect CPUs)
pytest -m "e2e" -n auto --browser=chrome --headless
```

Markers are defined in `pytest.ini`. Each test gets a fresh browser thanks to the function-scoped `driver` fixture defined in `conftest.py`.

---

## Reports & artifacts
- **pytest-html**: Generated when `--html` is provided; screenshots from failures are attached automatically.
- **Allure**: `--alluredir=reports/allure-results` produces raw data. Serve locally with `allure serve reports/allure-results` if you have the CLI installed.
- **Coverage**: `coverage html -d reports/coverage` builds an HTML dashboard. CI publishes the aggregate coverage as `coverage.json` for the shield badge.
- **Artifacts folder**: Screenshots are stored under `artifacts/screenshots/` whenever a test fails.

---

## Continuous integration
GitHub Actions workflow: `.github/workflows/ci.yml`

Job summary:
- **Lint**: Runs `black` and `flake8`.
- **Unit**: Executes unit tests with coverage and uploads `reports/unit_report.html`, `reports/coverage.xml`, and `htmlcov/` artifacts.
- **E2E**: Runs the browser suite, captures screenshots, and publishes Allure raw data.
- **Deploy Allure Report**: Renders the latest Allure dashboard and coverage badge to GitHub Pages at `https://sharair.github.io/pytest_and_selenium/`.

Dynamic coverage badge updates are handled during the pages deployment and point to the JSON hosted on GitHub Pages.

---

## Project structure
```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       ├── config.yml
│       └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/ci.yml
├── artifacts/                    # Screenshots saved by pytest hook
├── reports/                      # HTML, Allure, and coverage outputs
├── src/
│   ├── config.py                 # Settings dataclass & env parsing helpers
│   └── pages/
│       ├── base_page.py          # Common waits/utilities for page objects
│       ├── inventory_page.py     # Inventory interactions & assertions
│       └── login_page.py         # Login form actions
├── tests/
│   ├── e2e/
│   │   ├── test_add_to_cart.py
│   │   └── test_login.py
│   └── unit/
│       ├── test_base_page.py
│       ├── test_config.py
│       ├── test_config_users.py
│       ├── test_inventory_page.py
│       └── test_login_page.py
├── conftest.py                   # Pytest fixtures, CLI options, screenshots
├── pytest.ini                    # Markers, default test settings
├── requirements.txt
├── .env.example
├── LICENSE
└── README.md
```

---

## Troubleshooting
- **`ModuleNotFoundError: dotenv`** &rarr; Ensure dependencies are installed with `pip install -r requirements.txt`.
- **Browser fails to start** &rarr; Confirm Chrome/Firefox is installed locally; Selenium Manager resolves drivers automatically.
- **Pre-run check skips suite** &rarr; Set `SKIP_PRERUN_CHECK=true` to bypass the availability probe when running against local/staging environments.
- **Allure command not found** &rarr; Install the Allure CLI or open the generated HTML report instead (`pytest-html`).

---

## License
Distributed under the [MIT License](LICENSE).

