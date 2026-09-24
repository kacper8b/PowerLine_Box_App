"""Tests for config.py's dev-vs-frozen path resolution (ICON_PATH, _CONFIG_TEMPLATES_DIR).

This logic runs at module import time based on sys.frozen (set by the
PyInstaller bootloader in a built .exe, absent otherwise). To exercise both
branches, the module is reloaded after monkeypatching sys.frozen/sys.executable,
and reloaded again afterwards to restore the normal (non-frozen) state so other
tests importing powerline_box.config see the correct values.
"""
import importlib
import os
import sys

from powerline_box import config


def test_dev_mode_points_into_the_repo_config_and_packaging_folders():
    importlib.reload(config)  # clean, non-frozen baseline

    assert not getattr(sys, "frozen", False)
    assert os.path.basename(config._CONFIG_TEMPLATES_DIR) == "config"
    assert os.path.isdir(config._CONFIG_TEMPLATES_DIR)
    assert os.path.basename(os.path.dirname(config.ICON_PATH)) == "packaging"
    assert os.path.basename(config.ICON_PATH) == "powerline-box.ico"


def test_frozen_mode_points_flat_next_to_the_exe(monkeypatch, tmp_path):
    fake_exe = tmp_path / "powerline-box.exe"
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(fake_exe))
    try:
        importlib.reload(config)

        assert config._CONFIG_TEMPLATES_DIR == str(tmp_path)
        assert config.ICON_PATH == str(tmp_path / "powerline-box.ico")
    finally:
        # Undo sys.frozen/sys.executable now (not at fixture teardown time)
        # and reload so later tests see the normal, non-frozen paths again.
        monkeypatch.undo()
        importlib.reload(config)
