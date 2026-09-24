import config
import gui
import panel.panel as panel

# USED interfaces:
id_button = {
    'send': "panel_main_send",
    'init': "panel_main_init",
    'on': "panel_main_on",
    'off': "panel_main_off",
    'safe_on': "panel_main_send",
    'safe_off': "panel_main_send",
    'edit':  "panel_main_edit",
    'save': "panel_main_save",
    'cancel': "panel_main_cancel",
    'dpc': "panel_dpc"
}

id_entry = {
    'send': "panel_main_send"
}


def create(frame):
    """create_buttons
    ----------------------------------------------------------------------------------------------------------------
    """

    # Create Main buttons and Entry
    buttons_initial_position_x = config.panel_main['buttons_initial_position_x']
    buttons_initial_position_y = config.panel_main['buttons_initial_position_y']
    buttons_width = config.panel_main['buttons_width']
    buttons_height = config.panel_main['buttons_height']
    buttons_distance_x = config.panel_main['buttons_distance_x']
    buttons_distance_y = config.panel_main['buttons_distance_y']
    entry_width = config.panel_main['entry_width']
    entry_height = config.panel_main['entry_height']
    
    gui.create_entry(frame, entry_id=id_entry['send'], text="", height=entry_height, width=entry_width,
                     x=buttons_initial_position_x + 0*(buttons_width + buttons_distance_x) - 60,
                     y=buttons_initial_position_y + 0*(buttons_height + buttons_distance_y))
    
    gui.create_button(frame, text="SEND", button_id=id_button['send'],
                      width=buttons_width, height=buttons_height,
                      x=buttons_initial_position_x + 2*(buttons_width + buttons_distance_x),
                      y=buttons_initial_position_y + 0*(buttons_height + buttons_distance_y),
                      bg="#0C6046", fg="#ffffff",
                      active_background="#0C6046", active_foreground="#ffffff",
                      action=lambda: send())

    gui.create_button(frame, text="INIT", button_id=id_button['init'],
                      width=buttons_width, height=buttons_height,
                      x=buttons_initial_position_x + 0*(buttons_width + buttons_distance_x),
                      y=buttons_initial_position_y + 1*(buttons_height + buttons_distance_y),
                      bg="#0C6046", fg="#ffffff",
                      active_background="#0C6046", active_foreground="#ffffff",
                      action=lambda bt_id=id_button['init']: panel.init(bt_id))

    gui.create_button(frame, text="ON", button_id=id_button['on'],
                      width=buttons_width, height=buttons_height,
                      x=buttons_initial_position_x + 1*(buttons_width + buttons_distance_x),
                      y=buttons_initial_position_y + 1*(buttons_height + buttons_distance_y),
                      bg="#0C6046", fg="#ffffff",
                      active_background="#0C6046", active_foreground="#ffffff",
                      action=lambda: panel.on())

    gui.create_button(frame, text="OFF", button_id=id_button['off'],
                      width=buttons_width, height=buttons_height,
                      x=buttons_initial_position_x + 2*(buttons_width + buttons_distance_x),
                      y=buttons_initial_position_y + 1*(buttons_height + buttons_distance_y),
                      bg="#0C6046", fg="#ffffff",
                      active_background="#0C6046", active_foreground="#ffffff",
                      action=lambda: panel.off())

    gui.create_button(frame, text="DPC", button_id=id_button['dpc'],
                      width=buttons_width, height=buttons_height,
                      x=buttons_initial_position_x + 0*(buttons_width + buttons_distance_x),
                      y=buttons_initial_position_y + 2*(buttons_height + buttons_distance_y),
                      bg="#0C6046", fg="#ffffff",
                      active_background="#0C6046", active_foreground="#ffffff",
                      action=lambda bt_id=id_button['dpc']: panel.dpc(bt_id))

    # Create buttons for edit
    buttons_width = config.panel_main['buttons_modify_width']
    buttons_height = config.panel_main['buttons_modify_height']
    buttons_initial_position_x = config.panel_main['buttons_modify_initial_position_x']
    buttons_initial_position_y = config.panel_main['buttons_modify_initial_position_y']
    buttons_distance_x = config.panel_main['buttons_modify_distance_x']
    buttons_distance_y = config.panel_main['buttons_modify_distance_y']

    gui.create_button(frame, text="Edit", button_id=id_button['edit'],
                      width=buttons_width, height=buttons_height,
                      x=buttons_initial_position_x + 0*(buttons_width + buttons_distance_x),
                      y=buttons_initial_position_y + 0*(buttons_height + buttons_distance_y),
                      action=lambda: panel.edit(),
                      bg="#000000", fg="#ffffff",
                      active_background="#000000", active_foreground="#ffffff")

    gui.create_button(frame, text="Save", button_id=id_button['save'],
                      width=buttons_width, height=buttons_height,
                      x=buttons_initial_position_x + 0*(buttons_width + buttons_distance_x),
                      y=buttons_initial_position_y + 1*(buttons_height + buttons_distance_y),
                      action=lambda: panel.save(),
                      bg="#000000", fg="#ffffff",
                      active_background="#000000", active_foreground="#ffffff")

    gui.create_button(frame, text="Cancel", button_id=id_button['cancel'],
                      width=buttons_width, height=buttons_height,
                      x=buttons_initial_position_x + 0*(buttons_width + buttons_distance_x),
                      y=buttons_initial_position_y + 2*(buttons_height + buttons_distance_y),
                      action=lambda: panel.cancel(),
                      bg="#000000", fg="#ffffff",
                      active_background="#000000", active_foreground="#ffffff")

    hide_buttons()


def send():
    """send
    ----------------------------------------------------------------------------------------------------------------
    """
    msg = gui.get_entry(entry_id=id_entry['send']).get()
    panel.send(msg)


def show_buttons():
    """show_buttons
    ----------------------------------------------------------------------------------------------------------------
    """
    gui.show_button(button_id=id_button['save'])
    gui.show_button(button_id=id_button['cancel'])


def hide_buttons():
    """hide_buttons
    ----------------------------------------------------------------------------------------------------------------
    """
    gui.hide_button(button_id=id_button['save'])
    gui.hide_button(button_id=id_button['cancel'])