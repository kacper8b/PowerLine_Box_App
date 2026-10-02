import json

from powerline_box import config
from powerline_box.automation import storage


def _write(path, data):
    path.write_text(json.dumps(data), encoding="utf-8")


def test_list_scripts_empty_file(tmp_path, monkeypatch):
    path = tmp_path / "automation_scripts.json"
    _write(path, [])
    monkeypatch.setattr(config, "directory_automation", str(path))
    assert storage.list_scripts() == []


def test_save_and_load_script(tmp_path, monkeypatch):
    path = tmp_path / "automation_scripts.json"
    _write(path, [])
    monkeypatch.setattr(config, "directory_automation", str(path))

    script = {"name": "test", "repeat": 0, "steps": [{"type": "wait", "delay_ms": 500}]}
    assert storage.save_script(script) is True
    assert storage.list_scripts() == ["test"]
    assert storage.load_script("test") == script


def test_save_invalid_script_rejected(tmp_path, monkeypatch):
    path = tmp_path / "automation_scripts.json"
    _write(path, [])
    monkeypatch.setattr(config, "directory_automation", str(path))

    assert storage.save_script({"name": "", "repeat": 0, "steps": []}) is False


def test_save_overwrites_existing_by_name(tmp_path, monkeypatch):
    path = tmp_path / "automation_scripts.json"
    _write(path, [{"name": "test", "repeat": 0, "steps": []}])
    monkeypatch.setattr(config, "directory_automation", str(path))

    updated = {"name": "test", "repeat": 2, "steps": [{"type": "wait", "delay_ms": 100}]}
    assert storage.save_script(updated) is True
    assert json.loads(path.read_text(encoding="utf-8")) == [updated]


def test_delete_script(tmp_path, monkeypatch):
    path = tmp_path / "automation_scripts.json"
    _write(path, [{"name": "test", "repeat": 0, "steps": []}])
    monkeypatch.setattr(config, "directory_automation", str(path))

    assert storage.delete_script("test") is True
    assert storage.list_scripts() == []
    assert storage.delete_script("test") is False


def test_list_scripts_missing_file_returns_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "directory_automation", str(tmp_path / "missing.json"))
    assert storage.list_scripts() == []


def test_load_script_missing_file_returns_none(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "directory_automation", str(tmp_path / "missing.json"))
    assert storage.load_script("test") is None
