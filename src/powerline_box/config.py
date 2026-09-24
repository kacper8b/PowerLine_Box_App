
import json
import logging
import os
import sys
from shutil import copyfile

from powerline_box import theme

logger = logging.getLogger(__name__)

INIT_DELAY_DEFAULT = 1000
INIT_DELAY_MIN = 500
INIT_DELAY_MAX = 1200

windows = dict(
    width=1000,
    height=800,
    sidemenu_width=130,
    sidemenu_color=theme.LIGHT_GRAY,
    mainwindow_color=theme.LIGHT_GRAY,
    main_height=600,
    main_color=theme.WHITE,
    terminal_height=200,
    termnial_color=theme.WHITE,
)

panel_buttons = dict(
    frame_x=25,
    frame_y=195,
    frame_height=390,
    frame_width=820,
    buttons_id='panel_button_',
    buttons_columns=6,
    buttons_rows=10,
    buttons_initial_position_x=80,
    buttons_initial_position_y=35,
    buttons_width=120,
    buttons_height=30,
    buttons_distance_x=10,
    buttons_distance_y=5,
)

panel_main = dict(
    frame_x=25,
    frame_y=20,
    frame_height=170,
    frame_width=520,
    buttons_initial_position_x=80,
    buttons_initial_position_y=30,
    buttons_width=120,
    buttons_height=30,
    buttons_distance_x=10,
    buttons_distance_y=7,
    entry_width=250,
    entry_height=30,
    buttons_modify_width=50,
    buttons_modify_height=15,
    buttons_modify_initial_position_x=460,
    buttons_modify_initial_position_y=23,
    buttons_modify_distance_x=0,
    buttons_modify_distance_y=5,
)

panel_edit = dict(
    frame_x=550,
    frame_y=20,
    frame_height=170,
    frame_width=295,
    buttons_id='panel_main_',
    buttons_initial_position_x=50,
    buttons_initial_position_y=140,
    buttons_width=70,
    buttons_height=20,
    buttons_distance_x=10,
    buttons_distance_y=7,
    labels_initial_position_x=10,
    labels_initial_position_y=10,
    labels_distance_x=0,
    labels_distance_y=27,
    entry_id='panel_main_',
    entry_initial_position_x=90,
    entry_initial_position_y=20,
    entry_width=160,
    entry_height=20,
    entry_distance_x=10,
    entry_distance_y=7,    
)

terminal = dict(
    height=170,
    width=770,
    x=45,
    y=10,
    column_max=90,
    button_x=20,
    button_y=21,
    button_width=40,
    button_height=20
)

change_log = dict(
    height=250,
    width=765,
    x=50,
    y=300
)

directory_user = os.path.expanduser('~\\Documents\\PowerLine Box')
directory_config = directory_user + '\\config.json'
directory_panel = directory_user + '\\panel_buttons.json'

# Location of the default config templates and app icon.
# Frozen (PyInstaller) build: files are copied flat next to the .exe.
# Source run: files live in the repo's config/ and packaging/ folders.
if getattr(sys, "frozen", False):
    _APP_DIR = os.path.dirname(sys.executable)
    _CONFIG_TEMPLATES_DIR = _APP_DIR
    ICON_PATH = os.path.join(_APP_DIR, "powerline-box.ico")
else:
    _REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    _CONFIG_TEMPLATES_DIR = os.path.join(_REPO_ROOT, "config")
    ICON_PATH = os.path.join(_REPO_ROOT, "packaging", "powerline-box.ico")


def configuration_init():
    """get_button_text
    based on id (ID is assigned with create_button function
    --------------------------------------------------------------------------------------------------------------------
    """
    # create folder PowerLine Box
    if not os.path.isdir(directory_user):
        try:
            os.mkdir(directory_user)
        except OSError as error:
            logger.error("Creation of the directory %s failed: %s", directory_user, error)
        else:
            logger.info("Successfully created the directory %s", directory_user)

    # copy config files
    file_config = ['config.json', 'panel_buttons.json']
    for file in file_config:
        destination = os.path.join(directory_user, file)
        if not os.path.isfile(destination):
            try:
                copyfile(os.path.join(_CONFIG_TEMPLATES_DIR, file), destination)
            except OSError as error:
                logger.error("Copy of the file %s failed: %s", os.path.join(_CONFIG_TEMPLATES_DIR, file), error)
            else:
                logger.info("Successfully copy of the file %s", os.path.join(_CONFIG_TEMPLATES_DIR, file))


def get_init_delay():
    """Read the configured INIT command delay (ms) from the user's config.json,
    falling back to INIT_DELAY_DEFAULT if the file/key is missing or invalid.
    --------------------------------------------------------------------------------------------------------------------
    """
    try:
        with open(directory_config, encoding='utf-8') as json_data:
            data = json.load(json_data)
        return int(data.get('init delay', INIT_DELAY_DEFAULT))
    except (OSError, ValueError, TypeError) as error:
        logger.error("Could not read init delay from %s: %s", directory_config, error)
        return INIT_DELAY_DEFAULT
