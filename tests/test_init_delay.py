"""Tests for config.py's get_init_delay() reader/validator.

Uses a temp file for config.directory_config so tests never touch the real
user's Documents\\PowerLine Box\\config.json.
"""
import json

from powerline_box import config


def _write_config(path, data):
    path.write_text(json.dumps(data), encoding='utf-8')


def test_get_init_delay_returns_default_when_key_missing(monkeypatch, tmp_path):
    config_file = tmp_path / "config.json"
    _write_config(config_file, {"power line port": "COM4"})
    monkeypatch.setattr(config, "directory_config", str(config_file))

    assert config.get_init_delay() == config.INIT_DELAY_DEFAULT


def test_get_init_delay_returns_saved_value(monkeypatch, tmp_path):
    config_file = tmp_path / "config.json"
    _write_config(config_file, {"init delay": 700})
    monkeypatch.setattr(config, "directory_config", str(config_file))

    assert config.get_init_delay() == 700


def test_get_init_delay_falls_back_when_file_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "directory_config", str(tmp_path / "does_not_exist.json"))

    assert config.get_init_delay() == config.INIT_DELAY_DEFAULT


def test_get_init_delay_falls_back_on_invalid_value(monkeypatch, tmp_path):
    config_file = tmp_path / "config.json"
    _write_config(config_file, {"init delay": "not a number"})
    monkeypatch.setattr(config, "directory_config", str(config_file))

    assert config.get_init_delay() == config.INIT_DELAY_DEFAULT
