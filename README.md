# pytest-selenium-template - Demo project for `E2E/UI test automation`
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Selenium](https://img.shields.io/badge/selenium-4.35.0-43B02A?logo=selenium)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)]()
![unit tests](https://img.shields.io/badge/tests-unit-green)
[![pytest](https://img.shields.io/badge/tested_with-pytest-green.svg)]()
![parallel](https://img.shields.io/badge/parallel-pytest--xdist-yellowgreen)

![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
[![flake8](https://img.shields.io/badge/lint-flake8-lightgrey.svg)]()
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)
<!-- ![Allure](https://img.shields.io/badge/report-Allure-ff69b4) -->
[![CI](https://github.com/SharaiR/pytest_and_selenium/actions/workflows/ci.yml/badge.svg)](https://github.com/SharaiR/pytest_and_selenium/actions)
[Allure Report (latest)](https://sharair.github.io/pytest_and_selenium/)

A modern **Pytest + Selenium** template project with Page Object Model (POM), fixtures, screenshots on failures and ready-to-use reporting (HTML & Allure).

---

## Features
- ✅ **Pytest + Selenium 4** setup with Page Object Model
- ✅ **Reusable fixtures** (`conftest.py`)
- ✅ **Environment-driven users** (`.env`, `E2E_DEFAULT_USER`, `E2E_USERS_JSON`)
- ✅ **HTML & Allure reporting**
- ✅ **Crash screenshots** on failures
- ✅ **Parallel runs** with `pytest-xdist`
- ✅ **Code style & quality checks**: `flake8`, `black`, `pytest-cov`

---

## Quick start (local)
```bash
# 1. Create and activate virtual env
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run smoke tests (headless Chrome)
pytest -m "smoke" --browser=chrome --headless
```

---

## Users for e2e tests
- The default user is specified in .env as `E2E_DEFAULT_USER`.
- User logins and passwords are defined in `.env` in `E2E_USERS_JSON`.
Example .env:
```ini
# Default user for login
E2E_DEFAULT_USER=standard_user

# List of users in JSON format
E2E_USERS_JSON={"standard_user": "secret_sauce", "problem_user": "secret_sauce"}
```

By default, tests run as E2E_DEFAULT_USER.
To switch the user:
```bash
pytest --user=problem_user
```

---

## Running tests
Run E2E / smoke / regression
```bash
# Run smoke tests (Chrome headless, HTML report)
pytest -m "smoke" --browser=chrome --headless \
  --html=reports/report.html --self-contained-html

# Full run with Allure results
pytest -m "e2e or regression" --browser=chrome --headless \
  --alluredir=reports/allure-results

# View Allure report (if you have Allure installed)
allure serve reports/allure-results

# Full e2e launch (Chrome, headless, HTML report):
python3 -m pytest -m "e2e or smoke or regression" --browser=chrome --headless \
  --html=reports/report.html --self-contained-html
```

### 🔀 Parallel execution (pytest-xdist)

This project supports parallel test execution using **pytest-xdist**.

Examples:
```bash
# Run tests in 4 parallel workers
pytest -m "smoke" --browser=chrome --headless -n 4

# Parallel run (xdist auto)
pytest -m "e2e or regression" --browser=chrome --headless -n auto
```

ℹ️ _Each test gets its own browser instance (driver fixture has scope=function), so parallel execution is safe and isolated._

---

## Linting & formatting
Use `flake8` for linting and `black` for formatting.
```bash
# Run formatter
black .

# Run linter
flake8 .
```

Example useful `flake8` commands:
```bash
# Run targeted tests
flake8 src tests

flake8 src tests --count --statistics
flake8 src tests --select=E,F,W --show-source
```

---

## 📊 Unit tests & coverage
```bush
# Clean up old coverage artifacts
rm -rf .coverage .coverage.* reports/coverage

# Unit tests + coverage
python3 -m pytest tests/unit --cov=src --cov-report=term-missing

# HTML-report
python3 -m coverage html -d reports/coverage
```

---

## 📂 Project structure
```bash
.
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       ├── feature_request.md
│       └── config.yml
│   └── workflows/
│       └── ci.yml
├── artifacts/                      # Screenshots on failure
├── reports/                        # HTML/Allure outputs
│   ├── allure-results
│   └── coverage
├── src/                            # Page Object classes (LoginPage, InventoryPage, BasePage, etc.)
│   ├── config.py                   # env + CLI options
│   └── pages/
│       ├── base_page.py            # POM base class with waits & helpers
│       ├── login_page.py           # page object for login
│       └── inventory_page.py       # page object for inventory/actions
├── tests/
│   ├── e2e/                        # End-to-end UI tests
│   │   └── test_login.py
│   └── unit/                       # Unit tests for page objects & utils
│       ├── test_base_page.py
│       ├── test_config.py
│       ├── test_inventory_page.py
│       └── test_login_page.py
├── conftest.py                     # Pytest fixtures & hooks (screenshots, driver)
├── pytest.ini                      # Markers, defaults
├── requirements.txt
├── .gitignore
├── .env.example                    # Example env config
├── .coverage
├── .flake8
├── LICENSE
└── README.md
```

---

## License
This project is released under the MIT License.
