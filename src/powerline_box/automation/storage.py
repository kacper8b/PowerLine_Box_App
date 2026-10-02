"""Load/save/list/delete named automation scripts in config/automation_scripts.json
(the user's copy in Documents/PowerLine Box), mirroring panel/buttons.py's JSON handling.
----------------------------------------------------------------------------------------------------------------
"""
import json
import logging

from powerline_box import config
from powerline_box.automation import model

logger = logging.getLogger(__name__)


def _read_scripts_json():
    """_read_scripts_json
    ----------------------------------------------------------------------------------------------------------------
    """
    with open(config.directory_automation, encoding='utf-8') as json_data:
        return json.load(json_data)


def _write_scripts_json(scripts_json):
    """_write_scripts_json
    ----------------------------------------------------------------------------------------------------------------
    """
    with open(config.directory_automation, 'w', encoding='utf-8') as json_data:
        json.dump(scripts_json, json_data, ensure_ascii=False, indent=4)


def list_scripts():
    """list_scripts
    Returns the list of saved script names (empty list if the file is missing/invalid).
    ----------------------------------------------------------------------------------------------------------------
    """
    try:
        return [script['name'] for script in _read_scripts_json()]
    except (OSError, ValueError, KeyError, TypeError) as error:
        logger.error("Could not read automation scripts from %s: %s", config.directory_automation, error)
        return []


def load_script(name):
    """load_script
    Returns the saved script dict with the given name, or None if not found/unreadable.
    ----------------------------------------------------------------------------------------------------------------
    """
    try:
        scripts = _read_scripts_json()
    except (OSError, ValueError) as error:
        logger.error("Could not read automation scripts from %s: %s", config.directory_automation, error)
        return None

    for script in scripts:
        if script.get('name') == name:
            return script
    return None


def save_script(script):
    """save_script
    Creates or overwrites (by name) a saved script. Returns True on success.
    ----------------------------------------------------------------------------------------------------------------
    """
    if not model.validate_script(script):
        logger.error("Refusing to save invalid automation script: %r", script)
        return False

    try:
        scripts = _read_scripts_json()
    except (OSError, ValueError) as error:
        logger.error("Could not read automation scripts from %s: %s", config.directory_automation, error)
        scripts = []

    for idx, existing in enumerate(scripts):
        if existing.get('name') == script['name']:
            scripts[idx] = script
            break
    else:
        scripts.append(script)

    try:
        _write_scripts_json(scripts)
    except OSError as error:
        logger.error("Could not write automation scripts to %s: %s", config.directory_automation, error)
        return False
    return True


def delete_script(name):
    """delete_script
    Deletes a saved script by name. Returns True if a script was removed.
    ----------------------------------------------------------------------------------------------------------------
    """
    try:
        scripts = _read_scripts_json()
    except (OSError, ValueError) as error:
        logger.error("Could not read automation scripts from %s: %s", config.directory_automation, error)
        return False

    new_scripts = [script for script in scripts if script.get('name') != name]
    if len(new_scripts) == len(scripts):
        return False

    try:
        _write_scripts_json(new_scripts)
    except OSError as error:
        logger.error("Could not write automation scripts to %s: %s", config.directory_automation, error)
        return False
    return True
