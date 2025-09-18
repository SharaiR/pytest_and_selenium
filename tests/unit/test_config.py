import os
from importlib import reload

from src import config


def test_to_bool_parsing_returns_default():
    assert config._to_bool(None, True) is True


def test_to_bool_parsing():
    assert config._to_bool("1", False) is True
    assert config._to_bool("true", False) is True
    assert config._to_bool("YES", False) is True
    assert config._to_bool("on", False) is True
    assert config._to_bool("no", True) is False


def test_settings_reads_env(monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://test.local")
    monkeypatch.setenv("BROWSER", "FIREFOX")
    monkeypatch.setenv("HEADLESS", "true")
    monkeypatch.setenv("DEFAULT_TIMEOUT", "15")

    # Reload the module so that dataclass rereads env
    reload(config)
    
    s = config.settings
    assert s.base_url == "https://test.local"
    assert s.browser == "firefox"
    assert s.headless is True
    assert s.default_timeout == 15
