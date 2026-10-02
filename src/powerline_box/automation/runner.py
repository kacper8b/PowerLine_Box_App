"""Execution engine for automation scripts (see automation.model for the script/step format).

Runs flattened steps sequentially using Timer callbacks, the same mechanism
panel.controller uses for INIT/DPC sequences, but on its own, independent
Timer chain. Mutually exclusive with panel button presses / INIT / DPC via
panel.controller's shared PanelController state (see try_start_automation /
stop_automation / is_automation_running).
----------------------------------------------------------------------------------------------------------------
"""
import logging
from threading import Timer

from powerline_box import gui
from powerline_box import terminal_log as terminal_main
from powerline_box.automation import model
from powerline_box.panel import controller as panel
from powerline_box.uart import power_line

logger = logging.getLogger(__name__)

# delay after a command step before moving on, mirrors controller.command_send's default
DEFAULT_STEP_DELAY_S = 0.5


class _RunnerState:
    def __init__(self):
        self.timer = None
        self.flat_steps = []
        self.index = 0
        self.remaining_repeats = 0
        self.on_step = None
        self.on_finished = None


_state = _RunnerState()


def is_running():
    """is_running
    ----------------------------------------------------------------------------------------------------------------
    """
    return panel.is_automation_running()


def run(script, on_step=None, on_finished=None):
    """run
    Starts executing `script` (a name is only required to save a script, not to run
    it). Returns True if the run started, False if blocked (not connected, invalid
    steps, already running, or a panel/INIT/DPC action is in progress).
    on_step(index, step) is called just before each flattened step executes.
    on_finished(reason) is called once the run ends ("completed", "stopped", "error").
    ----------------------------------------------------------------------------------------------------------------
    """
    if is_running():
        return False
    if not power_line.is_connected():
        terminal_main.add_text("not connected")
        return False
    if not isinstance(script, dict) or not model.validate_steps(script.get('steps')):
        logger.error("Refusing to run invalid automation script: %r", script)
        return False
    repeat = script.get('repeat')
    if not (isinstance(repeat, int) and not isinstance(repeat, bool) and repeat >= model.SCRIPT_REPEAT_FOREVER):
        logger.error("Refusing to run automation script with invalid repeat count: %r", script)
        return False
    if not panel.try_start_automation():
        return False

    _state.flat_steps = model.flatten_steps(script['steps'])
    _state.index = 0
    _state.remaining_repeats = repeat  # 0 means "until stopped"
    _state.on_step = on_step
    _state.on_finished = on_finished

    if not _state.flat_steps:
        _finish("completed")
        return True

    _run_next_step()
    return True


def stop():
    """stop
    ----------------------------------------------------------------------------------------------------------------
    """
    if is_running():
        _cancel_timer()
        _finish("stopped")


def _cancel_timer():
    """_cancel_timer
    ----------------------------------------------------------------------------------------------------------------
    """
    if _state.timer is not None:
        _state.timer.cancel()
        _state.timer = None


def _finish(reason):
    """_finish
    ----------------------------------------------------------------------------------------------------------------
    """
    _cancel_timer()
    panel.stop_automation()
    callback = _state.on_finished
    _state.flat_steps = []
    _state.index = 0
    _state.on_step = None
    _state.on_finished = None
    if callback is not None:
        callback(reason)


def _run_next_step():
    """_run_next_step
    ----------------------------------------------------------------------------------------------------------------
    """
    if not is_running():
        return  # stopped from elsewhere

    if _state.index >= len(_state.flat_steps):
        _state.index = 0
        if _state.remaining_repeats != model.SCRIPT_REPEAT_FOREVER:
            _state.remaining_repeats -= 1
            if _state.remaining_repeats <= 0:
                _finish("completed")
                return

    step = _state.flat_steps[_state.index]
    _state.index += 1

    if _state.on_step is not None:
        _state.on_step(_state.index - 1, step)

    if step['type'] == model.STEP_WAIT:
        _schedule_next(step['delay_ms'] / 1000.0)
        return

    if not power_line.is_connected():
        terminal_main.add_text("not connected")
        _finish("error")
        return

    cmd = (step['command'].lower() + "\r\n").encode('utf-8')
    sent = power_line.send(cmd)
    terminal_main.add_text((sent.decode('utf-8')).replace('\r\n', '') + " (" + step['name'] + ")")

    _schedule_next(DEFAULT_STEP_DELAY_S)


def _schedule_next(delay_s):
    """_schedule_next
    ----------------------------------------------------------------------------------------------------------------
    """
    _state.timer = Timer(delay_s, lambda: gui.run_on_ui_thread(_run_next_step))
    _state.timer.start()
