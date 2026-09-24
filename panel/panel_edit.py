import config
import gui
import tkinter as tk
import panel.panel as panel

# USED interfaces:
id_button = {
    'ok': "panel_edit_ok",
    'clear': "panel_edit_clear",
    'delete': "panel_edit_delete",
}

id_entry = {
    'name': "panel_edit_name",
    'command': "panel_edit_command",
    'bg': "panel_edit_bg",
    'font bg': "panel_edit_font_bg"
}

id_label = {
    'name': "panel_edit_name",
    'command': "panel_edit_command",
    'background': "panel_edit_background",
    'font color': "panel_edit_color"
}

panel_edit_frame = tk.Frame


def create(frame):
    """create_buttons
    ----------------------------------------------------------------------------------------------------------------
    """
    global panel_edit_frame
    panel_edit_frame = frame
    
    # Create Entries
    entry_initial_position_x = config.panel_edit['entry_initial_position_x']
    entry_initial_position_y = config.panel_edit['entry_initial_position_y']
    entry_width = config.panel_edit['entry_width']
    entry_height = config.panel_edit['entry_height']
    entry_distance_x = config.panel_edit['entry_distance_x']
    entry_distance_y = config.panel_edit['entry_distance_y']

    gui.create_entry(frame, entry_id=id_entry['name'], text="", height=entry_height, width=entry_width,
                     x=entry_initial_position_x + 0*(entry_width + entry_distance_x),
                     y=entry_initial_position_y + 0*(entry_height + entry_distance_y))

    gui.create_entry(frame, entry_id=id_entry['command'], text="", height=entry_height, width=entry_width,
                     x=entry_initial_position_x + 0*(entry_width + entry_distance_x),
                     y=entry_initial_position_y + 1*(entry_height + entry_distance_y))

    gui.create_entry(frame, entry_id=id_entry['bg'], text="", height=entry_height, width=entry_width,
                     x=entry_initial_position_x + 0*(entry_width + entry_distance_x),
                     y=entry_initial_position_y + 2*(entry_height + entry_distance_y))

    gui.create_entry(frame, entry_id=id_entry['font bg'], text="", height=entry_height, width=entry_width,
                     x=entry_initial_position_x + 0*(entry_width + entry_distance_x),
                     y=entry_initial_position_y + 3*(entry_height + entry_distance_y))

    # Create Labels
    labels_initial_position_x = config.panel_edit['labels_initial_position_x']
    labels_initial_position_y = config.panel_edit['labels_initial_position_y']
    labels_distance_x = config.panel_edit['labels_distance_x']

    gui.create_label(frame, label_id=id_label['name'], text="Name:",
                     x=labels_initial_position_x + 0*(labels_distance_x),
                     y=labels_initial_position_y + 0*(entry_distance_y + entry_height))

    gui.create_label(frame, label_id=id_label['command'], text="Command:",
                     x=labels_initial_position_x + 0*(labels_distance_x),
                     y=labels_initial_position_y + 1*(entry_distance_y + entry_height))

    gui.create_label(frame, label_id=id_label['background'], text="Background:",
                     x=labels_initial_position_x + 0*(labels_distance_x),
                     y=labels_initial_position_y + 2*(entry_distance_y + entry_height))

    gui.create_label(frame, label_id=id_label['font color'], text="Font color:",
                     x=labels_initial_position_x + 0*(labels_distance_x),
                     y=labels_initial_position_y + 3*(entry_distance_y + entry_height))

    # Create Buttons
    buttons_initial_position_x = config.panel_edit['buttons_initial_position_x']
    buttons_initial_position_y = config.panel_edit['buttons_initial_position_y']
    buttons_width = config.panel_edit['buttons_width']
    buttons_height = config.panel_edit['buttons_height']
    buttons_distance_x = config.panel_edit['buttons_distance_x']
    buttons_distance_y = config.panel_edit['buttons_distance_y']

    gui.create_button(frame, text="OK", button_id=id_button['ok'],
                      width=buttons_width, height=buttons_height,
                      x=buttons_initial_position_x + 0*(buttons_width + buttons_distance_x),
                      y=buttons_initial_position_y + 0*(buttons_height + buttons_distance_y),
                      action=lambda: panel.ok())

    gui.create_button(frame, text="Clear", button_id=id_button['clear'],
                      width=buttons_width, height=buttons_height,
                      x=buttons_initial_position_x + 1*(buttons_width + buttons_distance_x),
                      y=buttons_initial_position_y + 0*(buttons_height + buttons_distance_y),
                      action=lambda: panel.clear())

    gui.create_button(frame, text="Delete", button_id=id_button['delete'],
                      width=buttons_width, height=buttons_height,
                      x=buttons_initial_position_x + 2*(buttons_width + buttons_distance_x),
                      y=buttons_initial_position_y + 0*(buttons_height + buttons_distance_y),
                      action=lambda: panel.delete())


def show():
    """show
    ----------------------------------------------------------------------------------------------------------------
    """
    panel_edit_frame.place(x=config.panel_edit['frame_x'], y=config.panel_edit['frame_y'])


def hide():
    """show
    ----------------------------------------------------------------------------------------------------------------
    """
    panel_edit_frame.pack()
    panel_edit_frame.pack_forget()


def send_data(name=None, command=None, bg=None, fg=None):
    """send_data
    ----------------------------------------------------------------------------------------------------------------
    """
    if name is not None:
        gui.config_entry(entry_id=id_entry['name'], text=name)
    if command is not None:
        gui.config_entry(entry_id=id_entry['command'], text=command)
    if bg is not None:
        gui.config_entry(entry_id=id_entry['bg'], text=bg)
    if fg is not None:
        gui.config_entry(entry_id=id_entry['font bg'], text=fg)


def get_data(name=None, command=None, bg=None, fg=None):
    """get_data
    ----------------------------------------------------------------------------------------------------------------
    """
    if name is not None:
        return gui.get_entry(entry_id=id_entry['name']).get()
    if command is not None:
        return gui.get_entry(entry_id=id_entry['command']).get()
    if bg is not None:
        return gui.get_entry(entry_id=id_entry['bg']).get()
    if fg is not None:
        return gui.get_entry(entry_id=id_entry['font bg']).get()
