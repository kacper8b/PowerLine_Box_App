import json

from powerline_box import config
from powerline_box import gui
from powerline_box.panel import controller as panel

# USED interfaces:
id_button = {
    'button': "button_",
}

buttons_copy = None


def create_buttons(frame):
    """create_buttons
    ----------------------------------------------------------------------------------------------------------------
    """
    buttons_columns = config.panel_buttons['buttons_columns']
    buttons_rows = config.panel_buttons['buttons_rows']
    buttons_initial_position_x = config.panel_buttons['buttons_initial_position_x']
    buttons_initial_position_y = config.panel_buttons['buttons_initial_position_y']
    buttons_width = config.panel_buttons['buttons_width']
    buttons_height = config.panel_buttons['buttons_height']
    buttons_distance_x = config.panel_buttons['buttons_distance_x']
    buttons_distance_y = config.panel_buttons['buttons_distance_y']

    idx = 0
    for y in range(buttons_rows):
        for x in range(buttons_columns):
            idx += 1
            button_id = "{0}{1}".format(id_button['button'], idx)
            gui.create_button(frame, text="", button_id=button_id,
                              width=buttons_width, height=buttons_height,
                              x=buttons_initial_position_x+x*(buttons_width + buttons_distance_x),
                              y=buttons_initial_position_y+y*(buttons_height + buttons_distance_y),
                              bg="#660D0D", fg="#ffffff",
                              active_background="#660D0D", active_foreground="#ffffff",
                              action=lambda b_id=button_id: panel.panel_button_pressed(b_id, ""))


def show_buttons():
    """show buttons
    ----------------------------------------------------------------------------------------------------------------
    """

    buttons_columns = config.panel_buttons['buttons_columns']
    buttons_rows = config.panel_buttons['buttons_rows']

    idx = 0
    for y in range(buttons_rows):
        for x in range(buttons_columns):
            idx += 1
            gui.show_button(button_id="{0}{1}".format(id_button['button'], idx))


def hide_buttons(hide_all=False):
    """hide buttons
    ----------------------------------------------------------------------------------------------------------------
    """
    buttons_columns = config.panel_buttons['buttons_columns']
    buttons_rows = config.panel_buttons['buttons_rows']

    idx = 0
    for y in range(buttons_rows):
        for x in range(buttons_columns):
            idx += 1
            name = gui.get_button_data("{0}{1}".format(id_button['button'], idx), text=True)
            if name == "" or hide_all:
                gui.hide_button(button_id="{0}{1}".format(id_button['button'], idx))


def config_buttons():
    """config buttons
    ----------------------------------------------------------------------------------------------------------------
    assign the name/commands based on json config file
    """
    buttons_columns = config.panel_buttons['buttons_columns']
    buttons_rows = config.panel_buttons['buttons_rows']
    button_id = None

    # read config file
    with open(config.directory_panel, encoding='utf-8') as json_data:
        buttons_json = json.load(json_data)
        json_data.close()

        # clear all buttons
        idx = 0
        for y in range(buttons_rows):
            for x in range(buttons_columns):
                idx += 1
                button_id = "{0}{1}".format(id_button['button'], idx)
                gui.config_button(button_id=button_id, text="",
                                  action=lambda b_id=button_id: panel.panel_button_pressed(b_id, ""))

        # config button
        for button in buttons_json:
            name = button['name']
            command = button['command']
            column = button['x']
            row = button['y']
            bg = button['bg']
            fg = button['fg']

            idx = 0
            for y in range(buttons_rows):
                for x in range(buttons_columns):
                    idx += 1
                    button_id = "{0}{1}".format(id_button['button'], idx)

                    if x == column and y == row:
                        gui.config_button(button_id=button_id, text=name,
                                          action=lambda b_id=button_id,
                                          cmd=command: panel.panel_button_pressed(b_id, cmd),
                                          bg=bg, fg=fg, active_background=bg, active_foreground=fg)
                        # assign new id
                        button['id'] = button_id
                        break

    # write config file
    with open(config.directory_panel, 'w', encoding='utf-8') as json_data:
        json.dump(buttons_json, json_data, ensure_ascii=False, indent=4)
        json_data.close()


def edit_button(button_id, new_command, new_text, new_bg, new_fg):
    """edit_button
    ----------------------------------------------------------------------------------------------------------------
    """
    new_button = True

    # read config file
    with open(config.directory_panel, 'r', encoding='utf-8') as json_data:
        buttons_json = json.load(json_data)
        json_data.close()

    # edit button
    for button_json in buttons_json:
        if button_json['id'] == button_id:
            button_json['name'] = new_text
            button_json['command'] = new_command
            button_json['bg'] = new_bg
            button_json['fg'] = new_fg
            new_button = False
            break

    # create new button
    if new_button:

        buttons_columns = config.panel_buttons['buttons_columns']
        buttons_rows = config.panel_buttons['buttons_rows']

        idx = 0
        for y in range(buttons_rows):
            for x in range(buttons_columns):
                idx += 1
                if button_id == "{0}{1}".format(id_button['button'], idx):
                    button = {
                        'id': button_id,
                        'name': new_text,
                        'command': new_command,
                        'x': x,
                        'y': y,
                        'bg': new_bg,
                        'fg': new_fg
                    }
                    buttons_json.append(button)

    # write config file
    with open(config.directory_panel, 'w', encoding='utf-8') as json_data:
        json.dump(buttons_json, json_data, ensure_ascii=False, indent=4)
        json_data.close()

    # refresh buttons
    config_buttons()


def delete_button(button_id):
    """edit_button
    ----------------------------------------------------------------------------------------------------------------
    """
    # read config file
    with open(config.directory_panel, 'r', encoding='utf-8') as json_data:
        buttons_json = json.load(json_data)
        json_data.close()

    idx = 0
    for button_json in buttons_json:
        if button_json['id'] == button_id:
            del buttons_json[idx]
            break
        idx = idx + 1

    # write config file
    with open(config.directory_panel, 'w', encoding='utf-8') as json_data:
        json.dump(buttons_json, json_data, ensure_ascii=False, indent=4)
        json_data.close()

    # refresh buttons
    config_buttons()


def copy_buttons():
    """copy_buttons
    ----------------------------------------------------------------------------------------------------------------
    """
    global buttons_copy

    # read config file
    with open(config.directory_panel, 'r', encoding='utf-8') as json_data:
        buttons_copy = json.load(json_data)
        json_data.close()


def restore_buttons():
    """restore_buttons
    ----------------------------------------------------------------------------------------------------------------
    """
    if buttons_copy is not None:
        # write config file
        with open(config.directory_panel, 'w', encoding='utf-8') as json_data:
            json.dump(buttons_copy, json_data, ensure_ascii=False, indent=4)
            json_data.close()

        # refresh buttons
        config_buttons()


def select_button_effect_activate(button_id):
    """select_button_effect_activate
    ----------------------------------------------------------------------------------------------------------------
    """
    buttons_width = config.panel_buttons['buttons_width']
    buttons_height = config.panel_buttons['buttons_height']

    gui.config_button(button_id=button_id, width=0.9 * buttons_width, height=0.9 * buttons_height)


def select_button_effect_deactivate(button_id):
    """select_button_effect_deactivate
    ----------------------------------------------------------------------------------------------------------------
    """
    buttons_width = config.panel_buttons['buttons_width']
    buttons_height = config.panel_buttons['buttons_height']

    gui.config_button(button_id=button_id, width=buttons_width, height=buttons_height)
