"""In-memory editing state and actions for the Automation window: builds/edits a
script, saves/loads/deletes named scripts, and starts/stops a run via automation.runner.
----------------------------------------------------------------------------------------------------------------
"""
import logging

from powerline_box import config
from powerline_box import gui
from powerline_box import terminal_log as terminal_main
from powerline_box.automation import model
from powerline_box.automation import runner
from powerline_box.automation import storage
from powerline_box.panel import buttons as panel_buttons
from powerline_box.panel import controller as panel_controller

logger = logging.getLogger(__name__)

# USED interfaces:
id_button = {
    'quick_init': "automation_quick_init",
    'quick_on': "automation_quick_on",
    'quick_off': "automation_quick_off",
    'quick_up': "automation_quick_up",
    'quick_stop': "automation_quick_stop",
    'quick_down': "automation_quick_down",
}

id_listbox = {
    'scripts': "automation_scripts",
    'steps': "automation_steps",
}

id_entry = {
    'script_name': "automation_script_name",
    'wait_ms': "automation_wait_ms",
    'loop_repeat': "automation_loop_repeat",
    'script_repeat': "automation_script_repeat",
}

id_dropdown = {
    'command': "automation_command",
    'sequence': "automation_sequence",
}

_current_script = model.new_script(name="")

# maps each row shown in the steps listbox back to its top-level step index in
# _current_script['steps'] - a container step (loop/preset/script) can render as
# several rows, which all map back to that same top-level step index
_row_to_step_index = []

_INDENT_UNIT = "    "


def _step_lines(step, depth):
    """_step_lines
    Returns the display line(s) for `step` at the given nesting depth. depth 0 (a
    top-level step) has no indent/bullet; deeper steps are indented and bulleted.
    A loop or an inserted script is shown expanded (header + its own steps, one
    level deeper); a preset (Init/Power On/Power Off/DPC) is always shown collapsed
    as just its name, since it's a fixed, non-editable sequence.
    ----------------------------------------------------------------------------------------------------------------
    """
    indent = _INDENT_UNIT * depth
    prefix = indent + ("- " if depth > 0 else "")

    if step['type'] == model.STEP_COMMAND:
        return [prefix + "Command: {0} ({1})".format(step['name'], step['command'])]
    if step['type'] == model.STEP_WAIT:
        return [prefix + "Wait {0} ms".format(step['delay_ms'])]
    if step['type'] == model.STEP_PRESET:
        return [prefix + step['name']]
    if step['type'] in (model.STEP_LOOP, model.STEP_SCRIPT):
        header = prefix + ("Loop x{0}:".format(step['repeat']) if step['type'] == model.STEP_LOOP else step['name'])
        lines = [header]
        for inner_step in step['steps']:
            lines.extend(_step_lines(inner_step, depth + 1))
        return lines
    return [prefix + "?"]


def _selected_step_indices():
    """_selected_step_indices
    Converts the listbox's selected rows into the unique top-level step indices they
    belong to (a loop's header/sub-rows all map to the same index).
    ----------------------------------------------------------------------------------------------------------------
    """
    indices = []
    for row in gui.get_listbox_selection(id_listbox['steps']):
        if row < len(_row_to_step_index):
            step_index = _row_to_step_index[row]
            if step_index not in indices:
                indices.append(step_index)
    return indices


def refresh():
    """refresh
    Redraws the step list, the saved-scripts list, and the command/sequence
    dropdowns' choices. A loop or inserted script is shown expanded (header + its
    own indented steps); a preset (Init/Power On/Power Off/DPC) is shown collapsed.
    ----------------------------------------------------------------------------------------------------------------
    """
    global _row_to_step_index
    lines = []
    row_to_step_index = []

    for step_index, step in enumerate(_current_script['steps']):
        step_lines = _step_lines(step, depth=0)
        lines.extend(step_lines)
        row_to_step_index.extend([step_index] * len(step_lines))

    _row_to_step_index = row_to_step_index
    gui.set_listbox_items(id_listbox['steps'], lines)
    gui.set_listbox_items(id_listbox['scripts'], storage.list_scripts())

    button_names = [button['name'] for button in panel_buttons.list_buttons()]
    gui.set_dropdown_values(id_dropdown['command'], button_names)

    sequence_values = list(_SEQUENCE_PRESETS.keys()) + storage.list_scripts()
    gui.set_dropdown_values(id_dropdown['sequence'], sequence_values)

    gui.config_entry(entry_id=id_entry['script_name'], text=_current_script['name'])
    gui.config_entry(entry_id=id_entry['script_repeat'], text=str(_current_script['repeat']))


def new_script():
    """new_script
    ----------------------------------------------------------------------------------------------------------------
    """
    global _current_script
    if runner.is_running():
        return
    _current_script = model.new_script(name="")
    refresh()


def load_selected():
    """load_selected
    ----------------------------------------------------------------------------------------------------------------
    """
    global _current_script
    if runner.is_running():
        return
    names = storage.list_scripts()
    selection = gui.get_listbox_selection(id_listbox['scripts'])
    if not selection:
        return
    script = storage.load_script(names[selection[0]])
    if script is not None:
        _current_script = script
        refresh()


def save_as():
    """save_as
    ----------------------------------------------------------------------------------------------------------------
    """
    if runner.is_running():
        return
    name = gui.get_entry(id_entry['script_name']).get().strip()
    if name == "":
        terminal_main.add_text("automation: enter a script name before saving")
        return

    _current_script['name'] = name
    _current_script['repeat'] = _read_script_repeat()
    if storage.save_script(_current_script):
        terminal_main.add_text("automation: saved script \"{0}\"".format(name))
        refresh()
    else:
        terminal_main.add_text("automation: could not save script \"{0}\"".format(name))


def delete_selected():
    """delete_selected
    ----------------------------------------------------------------------------------------------------------------
    """
    if runner.is_running():
        return
    names = storage.list_scripts()
    selection = gui.get_listbox_selection(id_listbox['scripts'])
    if not selection:
        return
    name = names[selection[0]]
    if storage.delete_script(name):
        terminal_main.add_text("automation: deleted script \"{0}\"".format(name))
        refresh()


def _read_wait_ms():
    """_read_wait_ms
    ----------------------------------------------------------------------------------------------------------------
    """
    try:
        return int(gui.get_entry(id_entry['wait_ms']).get())
    except (TypeError, ValueError):
        return None


def _read_loop_repeat():
    """_read_loop_repeat
    ----------------------------------------------------------------------------------------------------------------
    """
    try:
        return int(gui.get_entry(id_entry['loop_repeat']).get())
    except (TypeError, ValueError):
        return None


def _read_script_repeat():
    """_read_script_repeat
    ----------------------------------------------------------------------------------------------------------------
    """
    try:
        return int(gui.get_entry(id_entry['script_repeat']).get())
    except (TypeError, ValueError):
        return None


def add_command_step():
    """add_command_step
    ----------------------------------------------------------------------------------------------------------------
    """
    name = gui.get_dropdown_value(id_dropdown['command'])
    if name:
        _add_panel_button_step(name)


def _add_panel_button_step(button_name):
    """_add_panel_button_step
    Appends a Command step using the stored command of the panel button called
    `button_name` (used by both the dropdown picker and the Up/Stop/Down quick-add
    buttons). Logs an error if no such panel button exists.
    ----------------------------------------------------------------------------------------------------------------
    """
    if runner.is_running():
        return
    for button in panel_buttons.list_buttons():
        if button['name'] == button_name:
            _current_script['steps'].append(model.new_command_step(name=button['name'], command=button['command']))
            refresh()
            return
    terminal_main.add_text("automation: no panel button named \"{0}\" found".format(button_name))


def control_init(button_id):
    """control_init
    Starts/stops the INIT sequence directly on the hardware - identical to pressing
    INIT on the Control Panel (lets the user jog the motor while building a script).
    ----------------------------------------------------------------------------------------------------------------
    """
    panel_controller.init(button_id)


def control_on():
    """control_on
    Identical to pressing ON on the Control Panel.
    ----------------------------------------------------------------------------------------------------------------
    """
    panel_controller.on()


def control_off():
    """control_off
    Identical to pressing OFF on the Control Panel.
    ----------------------------------------------------------------------------------------------------------------
    """
    panel_controller.off()


def control_panel_button(button_id, name):
    """control_panel_button
    Sends the named panel button's stored command immediately - identical to
    pressing that button on the Control Panel (used for the Up/Stop/Down buttons).
    ----------------------------------------------------------------------------------------------------------------
    """
    for button in panel_buttons.list_buttons():
        if button['name'] == name:
            panel_controller.panel_button_pressed(button_id, button['command'])
            return
    terminal_main.add_text("automation: no panel button named \"{0}\" found".format(name))


def _build_init_steps():
    """_build_init_steps
    Mirrors the Control Panel's INIT sequence: safepwr 0 -> wait 500 ms -> pwr 0 ->
    wait 2000 ms -> safepwr 1 -> wait 500 ms -> init <delay from Settings>.
    ----------------------------------------------------------------------------------------------------------------
    """
    init_command = "init {0}".format(config.get_init_delay())
    return [
        model.new_command_step(name="Init: safepwr 0", command="safepwr 0"),
        model.new_wait_step(500),
        model.new_command_step(name="Init: pwr 0", command="pwr 0"),
        model.new_wait_step(2000),
        model.new_command_step(name="Init: safepwr 1", command="safepwr 1"),
        model.new_wait_step(500),
        model.new_command_step(name="Init: {0}".format(init_command), command=init_command),
    ]


def _build_on_steps():
    """_build_on_steps
    Mirrors the Control Panel's ON sequence: pwr 1 -> wait 1000 ms -> safepwr 1.
    ----------------------------------------------------------------------------------------------------------------
    """
    return [
        model.new_command_step(name="On: pwr 1", command="pwr 1"),
        model.new_wait_step(1000),
        model.new_command_step(name="On: safepwr 1", command="safepwr 1"),
    ]


def _build_off_steps():
    """_build_off_steps
    Mirrors the Control Panel's OFF command: safepwr 0.
    ----------------------------------------------------------------------------------------------------------------
    """
    return [model.new_command_step(name="Off: safepwr 0", command="safepwr 0")]


def _build_dpc_steps():
    """_build_dpc_steps
    Mirrors the Control Panel's DPC sequence: pwr 0(2s) -> safepwr 1(0.5s) ->
    pwr 1(2s) -> pwr 0(2s) -> pwr 1(7s) -> pwr 0(2s) -> pwr 1.
    ----------------------------------------------------------------------------------------------------------------
    """
    return [
        model.new_command_step(name="DPC: pwr 0", command="pwr 0"),
        model.new_wait_step(2000),
        model.new_command_step(name="DPC: safepwr 1", command="safepwr 1"),
        model.new_wait_step(500),
        model.new_command_step(name="DPC: pwr 1", command="pwr 1"),
        model.new_wait_step(2000),
        model.new_command_step(name="DPC: pwr 0", command="pwr 0"),
        model.new_wait_step(2000),
        model.new_command_step(name="DPC: pwr 1", command="pwr 1"),
        model.new_wait_step(7000),
        model.new_command_step(name="DPC: pwr 0", command="pwr 0"),
        model.new_wait_step(2000),
        model.new_command_step(name="DPC: pwr 1", command="pwr 1"),
    ]


_SEQUENCE_PRESETS = {
    "Init": _build_init_steps,
    "Power Off": _build_off_steps,
    "Power On": _build_on_steps,
    "DPC": _build_dpc_steps,
}


def preset_names():
    """preset_names
    ----------------------------------------------------------------------------------------------------------------
    """
    return list(_SEQUENCE_PRESETS.keys())


def add_sequence_step():
    """add_sequence_step
    Inserts the sequence/script chosen in the "Add sequence/script" dropdown: either
    one of the fixed hardware presets (Init/Power On/Power Off/DPC), shown collapsed,
    or a copy of a saved script's steps, shown expanded under its name.
    ----------------------------------------------------------------------------------------------------------------
    """
    if runner.is_running():
        return
    name = gui.get_dropdown_value(id_dropdown['sequence'])
    if not name:
        return

    builder = _SEQUENCE_PRESETS.get(name)
    if builder is not None:
        _current_script['steps'].append(model.new_preset_step(name=name, steps=builder()))
        refresh()
        return

    if _current_script['name'] != "" and name == _current_script['name']:
        terminal_main.add_text("automation: can't insert a script into itself")
        return

    script = storage.load_script(name)
    if script is None:
        terminal_main.add_text("automation: no saved script named \"{0}\" found".format(name))
        return
    _current_script['steps'].append(model.new_script_step(name=script['name'], steps=script['steps']))
    refresh()


def add_wait_step():
    """add_wait_step
    ----------------------------------------------------------------------------------------------------------------
    """
    if runner.is_running():
        return
    delay_ms = _read_wait_ms()
    if delay_ms is None or not (model.WAIT_MIN_MS <= delay_ms <= model.WAIT_MAX_MS):
        terminal_main.add_text("automation: enter a wait time between {0} and {1} ms".format(
            model.WAIT_MIN_MS, model.WAIT_MAX_MS))
        return
    _current_script['steps'].append(model.new_wait_step(delay_ms))
    refresh()


def remove_selected():
    """remove_selected
    ----------------------------------------------------------------------------------------------------------------
    """
    if runner.is_running():
        return
    for index in sorted(_selected_step_indices(), reverse=True):
        del _current_script['steps'][index]
    refresh()


def move_selected(offset):
    """move_selected
    Moves the single selected step up (offset=-1) or down (offset=+1).
    ----------------------------------------------------------------------------------------------------------------
    """
    if runner.is_running():
        return
    indices = _selected_step_indices()
    if len(indices) != 1:
        return
    index = indices[0]
    new_index = index + offset
    steps = _current_script['steps']
    if not (0 <= new_index < len(steps)):
        return
    steps[index], steps[new_index] = steps[new_index], steps[index]
    refresh()


def group_into_loop():
    """group_into_loop
    Wraps the selected contiguous command/wait steps into a single loop step.
    ----------------------------------------------------------------------------------------------------------------
    """
    if runner.is_running():
        return
    repeat = _read_loop_repeat()
    if repeat is None or not (model.LOOP_MIN_REPEAT <= repeat <= model.LOOP_MAX_REPEAT):
        terminal_main.add_text("automation: enter a loop repeat count between {0} and {1}".format(
            model.LOOP_MIN_REPEAT, model.LOOP_MAX_REPEAT))
        return

    indices = sorted(_selected_step_indices())
    if not indices:
        return
    if indices != list(range(indices[0], indices[-1] + 1)):
        terminal_main.add_text("automation: select a contiguous range of steps to group into a loop")
        return

    steps = _current_script['steps']
    selected_steps = steps[indices[0]:indices[-1] + 1]
    if any(step['type'] == model.STEP_LOOP for step in selected_steps):
        terminal_main.add_text("automation: loops can't be nested")
        return

    steps[indices[0]:indices[-1] + 1] = [model.new_loop_step(repeat=repeat, steps=selected_steps)]
    refresh()


def ungroup_loop():
    """ungroup_loop
    Replaces the selected loop step with its inner steps (its repeat count is discarded).
    ----------------------------------------------------------------------------------------------------------------
    """
    if runner.is_running():
        return
    indices = _selected_step_indices()
    if len(indices) != 1:
        return
    index = indices[0]
    steps = _current_script['steps']
    if steps[index]['type'] != model.STEP_LOOP:
        return
    steps[index:index + 1] = steps[index]['steps']
    refresh()


def _on_step(index, step):
    """_on_step
    `step` here is always a flattened command/wait step (runner.flatten_steps already
    expanded any loop/preset/script containers), so it always renders as one line.
    ----------------------------------------------------------------------------------------------------------------
    """
    terminal_main.add_text("automation: step {0} - {1}".format(index + 1, _step_lines(step, depth=0)[0]))


def _on_finished(reason):
    """_on_finished
    ----------------------------------------------------------------------------------------------------------------
    """
    terminal_main.add_text("automation: run {0}".format(reason))


def run():
    """run
    A script name is only required to save, not to run - this lets the user test
    an ad-hoc, unsaved sequence of steps.
    ----------------------------------------------------------------------------------------------------------------
    """
    _current_script['repeat'] = _read_script_repeat()
    if not model.validate_steps(_current_script['steps']):
        terminal_main.add_text("automation: add at least one valid step before running")
        return
    if not runner.run(_current_script, on_step=_on_step, on_finished=_on_finished):
        terminal_main.add_text("automation: could not start (not connected, or another action is in progress)")


def stop():
    """stop
    ----------------------------------------------------------------------------------------------------------------
    """
    runner.stop()
