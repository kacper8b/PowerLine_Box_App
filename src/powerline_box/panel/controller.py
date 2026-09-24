
from threading import Timer

from powerline_box import gui
from powerline_box import terminal_log as terminal_main
from powerline_box.panel import buttons as panel_buttons
from powerline_box.panel import edit as panel_edit
from powerline_box.panel import main_panel as panel_main
from powerline_box.uart import power_line


panel_state = {
    'normal': 0,
    'edit': 1,
}

events_list = {
    'power_on_0': 0,
    'power_on_1': 1,
    'init_0': 10,
    'init_1': 11,
    'init_2': 12,
    'init_3': 13,
    'command_send': 20,
    'command_send_double': 30,
    'dpc_0': 41,
    'dpc_1': 42,
    'dpc_2': 43,
    'dpc_3': 44,
    'dpc_4': 45,
    'dpc_5': 46,
    'dpc_6': 47,
}


class PanelController:
    """Holds the panel's runtime state (was a set of module-level globals)."""

    def __init__(self):
        self.current_button = {'id': None, 'bg': '#000000', 'fg': '#000000'}
        self.previous_button = {'id': None, 'bg': '#000000', 'fg': '#000000'}
        self.double_command = None
        self.double_command_comment = None
        self.state = panel_state['normal']
        self.event = None
        self.event_timer = None


_controller = PanelController()


def events():
    """events
    -----------------------------------------------------------------------------------------------------------------"""
    if _controller.event == events_list['power_on_0']:
        _controller.event = None
        command_send("pwr 1", new_event=events_list['power_on_1'], delay=1)
    elif _controller.event == events_list['power_on_1']:
        _controller.event = None
        command_send("safepwr 1", "Power ON")

    elif _controller.event == events_list['command_send']:
        _controller.event = None

    elif _controller.event == events_list['command_send_double']:
        _controller.event = None
        command_send(_controller.double_command, _controller.double_command_comment)

    elif _controller.event == events_list['init_0']:
        _controller.event = None
        if command_send("safepwr 0", new_event=events_list['init_1']):
            gui.config_button(button_id=_controller.current_button['id'], text="INIT in progress", bg="#660D0D", active_background="#660D0D")
    elif _controller.event == events_list['init_1']:
        _controller.event = None
        command_send("pwr 0", new_event=events_list['init_2'], delay=2)
    elif _controller.event == events_list['init_2']:
        _controller.event = None
        command_send("safepwr 1", new_event=events_list['init_3'])
    elif _controller.event == events_list['init_3']:
        _controller.event = None
        command_send("init 1000")
        gui.config_button(button_id=_controller.current_button['id'], text="INIT", bg="#0C6046", active_background="#0C6046")

    elif _controller.event == events_list['dpc_0']:
        _controller.event = None
        if command_send("pwr 0", new_event=events_list['dpc_1'], delay=2):
            gui.config_button(button_id=_controller.current_button['id'], text="DPC in progress", bg="#660D0D", active_background="#660D0D")
    elif _controller.event == events_list['dpc_1']:
        _controller.event = None
        command_send("safepwr 1", new_event=events_list['dpc_2'], delay=0.5)
    elif _controller.event == events_list['dpc_2']:
        _controller.event = None
        command_send("pwr 1", new_event=events_list['dpc_3'], delay=2)
    elif _controller.event == events_list['dpc_3']:
        _controller.event = None
        command_send("pwr 0", new_event=events_list['dpc_4'], delay=2)
    elif _controller.event == events_list['dpc_4']:
        _controller.event = None
        command_send("pwr 1", new_event=events_list['dpc_5'], delay=7)
    elif _controller.event == events_list['dpc_5']:
        _controller.event = None
        command_send("pwr 0", new_event=events_list['dpc_6'], delay=2)
    elif _controller.event == events_list['dpc_6']:
        _controller.event = None
        command_send("pwr 1")
        gui.config_button(button_id=_controller.current_button['id'], text="DPC", bg="#0C6046", active_background="#0C6046")


def create_event(new_event, time):
    """create events
    -----------------------------------------------------------------------------------------------------------------"""
    if _controller.event is None and _controller.state == panel_state['normal']:
        _controller.event = new_event
        # events() touches Tkinter widgets; the Timer fires on its own thread,
        # so hand off execution to the main thread via gui.run_on_ui_thread().
        _controller.event_timer = Timer(time, lambda: gui.run_on_ui_thread(events))
        _controller.event_timer.start()
        return True


def stop_event():
    """stop events
    -----------------------------------------------------------------------------------------------------------------"""
    _controller.event = None
    if _controller.event_timer is not None:
        _controller.event_timer.cancel()


def edit():
    """edit
    -----------------------------------------------------------------------------------------------------------------"""
    panel_buttons.show_buttons()
    panel_edit.show()
    panel_edit.send_data(name="", command="", bg="", fg="")  # clear data
    panel_main.show_buttons()

    if _controller.state == panel_state['normal']:
        _controller.state = panel_state['edit']
        panel_buttons.copy_buttons()


def cancel():
    """cancel
    -----------------------------------------------------------------------------------------------------------------"""
    panel_buttons.restore_buttons()
    panel_buttons.hide_buttons()
    panel_edit.hide()
    panel_edit.send_data(name="", command="", bg="", fg="")  # clear data
    panel_main.hide_buttons()

    _controller.state = panel_state['normal']
    panel_buttons.select_button_effect_deactivate(_controller.previous_button['id'])
    _controller.previous_button['id'] = None


def save():
    """save
    -----------------------------------------------------------------------------------------------------------------"""
    panel_buttons.hide_buttons()
    panel_edit.hide()
    panel_main.hide_buttons()

    _controller.state = panel_state['normal']
    panel_buttons.select_button_effect_deactivate(_controller.previous_button['id'])
    _controller.previous_button['id'] = None


def classify_ppc_command(command):
    """Classify a lowercase command string for frame generation.

    Returns (kind, parts):
      - ("single", (command,))       - a plain single-frame ppc command
      - ("double", (cmd1, cmd2))     - a double-frame ppc command split in two
      - ("other", (command,))        - any other command, sent as-is
    -----------------------------------------------------------------------------------------------------------------"""
    if "ppc" in command and command.count('d') == 1 and command.count('f') == 1:
        return "single", (command,)
    elif "ppc" in command and command.count('d') == 2 and command.count('f') == 2:
        d2 = command.rfind('d')
        cmd1 = command[0:d2]
        cmd2 = "ppc " + command[d2:]
        return "double", (cmd1, cmd2)
    else:
        return "other", (command,)


def panel_button_pressed(button_id, command=None):
    """command_send
    -----------------------------------------------------------------------------------------------------------------"""
    command = command.lower()

    if _controller.state == panel_state['normal'] and command is not None:
        # send command
        button_text = gui.get_button_data(button_id=button_id, text=True)

        kind, parts = classify_ppc_command(command)
        if kind == "single":
            command_send(command, button_text)
        elif kind == "double":
            cmd1, cmd2 = parts
            command_send(cmd1, button_text + ", part 1/2", new_event=events_list['command_send_double'])
            _controller.double_command = cmd2
            _controller.double_command_comment = button_text + ", part 2/2"
        else:
            command_send(command, button_text)
            create_event(events_list['command_send'], 0.5)

    elif _controller.state == panel_state['edit']:
        # edit button
        panel_edit.send_data(name=gui.get_button_data(button_id, text=True), command=command,
                             bg=gui.get_button_data(button_id, bg=True),
                             fg=gui.get_button_data(button_id, fg=True))

        _controller.current_button['id'] = button_id
        _controller.current_button['fg'] = gui.get_button_data(button_id, fg=True)
        _controller.current_button['bg'] = gui.get_button_data(button_id, bg=True)

        # button effect
        if _controller.previous_button['id'] is not None:
            panel_buttons.select_button_effect_deactivate(_controller.previous_button['id'])
        panel_buttons.select_button_effect_activate(_controller.current_button['id'])

        _controller.previous_button['id'] = button_id


def command_send(msg, comment=None, new_event=events_list['command_send'], delay=0.5):
    """command_send
    -----------------------------------------------------------------------------------------------------------------"""
    if _controller.state == panel_state['normal']:
        if not power_line.is_connected():
            terminal_main.add_text("not connected")
            return False
        else:
            print(msg)
            cmd = msg.lower() + "\r\n"
            cmd = cmd.encode('utf-8')

            cmd = power_line.send(cmd)

            if comment is None:
                terminal_main.add_text((cmd.decode('utf-8')).replace('\r\n', ''))
            else:
                terminal_main.add_text((cmd.decode('utf-8')).replace('\r\n', '') + " (" + comment + ")")

            create_event(new_event, delay)
            return True


def send(msg):
    """send
    -----------------------------------------------------------------------------------------------------------------"""
    command_send(msg)


def init(button_id):
    """init
    Save_off 0.5s
    pwr_0 2s
    Save_on 0.5s
    init
    -----------------------------------------------------------------------------------------------------------------"""
    if gui.get_button_data(button_id, text=True) == "INIT":
        if create_event(new_event=events_list['init_0'], time=0):
            _controller.current_button['id'] = button_id
    else:
        _controller.current_button['id'] = None
        gui.config_button(button_id=button_id, text="INIT", bg="#0C6046", active_background="#0C6046")
        stop_event()


def on():
    """on
    -----------------------------------------------------------------------------------------------------------------"""
    create_event(new_event=events_list['power_on_0'], time=0)


def off():
    """off
    -----------------------------------------------------------------------------------------------------------------"""
    command_send("safepwr 0", "Power OFF")


def dpc(button_id):
    """dpc
    Pwr_0 2s
    Safe_On 0.5s
    Pwr_1 2s
    Pwr_0 2s
    Pwr_1 7s
    Pwr_0 2s
    Pwr_1
    -----------------------------------------------------------------------------------------------------------------"""
    if gui.get_button_data(button_id, text=True) == "DPC":
        if create_event(new_event=events_list['dpc_0'], time=0):
            _controller.current_button['id'] = button_id
    else:
        _controller.current_button['id'] = None
        gui.config_button(button_id=button_id, text="DPC", bg="#0C6046", active_background="#0C6046")
        stop_event()


def ok():
    """ok
    -----------------------------------------------------------------------------------------------------------------"""

    if panel_edit.get_data(name=True) == "":
        panel_buttons.delete_button(button_id=_controller.current_button['id'])
    else:
        bg = panel_edit.get_data(bg=True)
        if gui.check_color(bg) is not True:
            bg = _controller.current_button['bg']
            panel_edit.send_data(bg=bg)

        fg = panel_edit.get_data(fg=True)
        if gui.check_color(fg) is not True:
            fg = _controller.current_button['fg']
            panel_edit.send_data(fg=fg)

        panel_buttons.edit_button(button_id=_controller.current_button['id'],
                                  new_command=panel_edit.get_data(command=True),
                                  new_text=panel_edit.get_data(name=True),
                                  new_bg=bg,
                                  new_fg=fg)

    panel_edit.send_data(name="", command="", bg="", fg="")  # clear data
    panel_buttons.select_button_effect_deactivate(_controller.previous_button['id'])
    _controller.previous_button['id'] = None


def clear():
    """clear
    -----------------------------------------------------------------------------------------------------------------"""
    panel_edit.send_data(name="", command="", bg="", fg="")  # clear data


def delete():
    """save_off
    -----------------------------------------------------------------------------------------------------------------"""
    panel_buttons.delete_button(button_id=_controller.current_button['id'])
    panel_edit.send_data(name="", command="", bg="", fg="")  # clear data
    panel_buttons.select_button_effect_deactivate(_controller.previous_button['id'])
    _controller.previous_button['id'] = None
