
import os
import json
import gui_terminal.terminal_main as terminal_main
from shutil import copyfile

windows = dict(
    width=1000,
    height=800,
    sidemenu_width=130,
    sidemenu_color="#D8DDE3",
    mainwindow_color="#D8DDE3",
    main_height=600,
    main_color="#FFFFFF",
    terminal_height=200,
    termnial_color="#FFFFFF",
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


def configuration_init():
    """get_button_text
    based on id (ID is assigned with create_button function
    --------------------------------------------------------------------------------------------------------------------
    """
    # create folder PowerLine Box
    if not os.path.isdir(directory_user):
        try:
            os.mkdir(directory_user)
        except OSError:
            print("Creation of the directory {0} failed".format(directory_user))
        else:
            print("Successfully created the directory {0}".format(directory_user))

    # copy config files
    file_config = ['\\config.json', '\\panel_buttons.json']
    for file in file_config:
        if not os.path.isfile(directory_user + file):
            try:
                copyfile(os.getcwd() + file, directory_user + file)
            except OSError:
                print("Copy of the file {0} failed".format(os.getcwd() + file))
            else:
                print("Successfully copy of the file {0}".format(os.getcwd() + file))
