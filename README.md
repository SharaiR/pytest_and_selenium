# pytest-selenium-template
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A starter project template for Pytest + Selenium with a Page Object Model (POM), fixtures, crash screenshots, HTML/Allure reports.


## Quick start (local)
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Unit tests and Coverage
```bush
# Clean up old coverage artifacts
rm -rf .coverage .coverage.* reports/coverage

# Unit tests + coverage
python3 -m pytest tests/unit --cov=src --cov-report=term-missing

# HTML-report
python3 -m coverage html -d reports/coverage
```

## License
MIT
