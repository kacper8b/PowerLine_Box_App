"""Tests for the Timer-driven INIT/DPC command sequences in panel/controller.py.

These sequences are normally driven by threading.Timer, which schedules each
step to run later on a background thread. To test the sequencing logic
deterministically (without waiting for real delays or touching Tkinter/serial
hardware), Timer is replaced with a test double that records pending calls
instead of firing them, and the test manually "fires" one step at a time via
run_next_timer() - mirroring exactly how the real Timer would trigger events()
once per scheduled delay, just without the wait.
"""
import pytest

from powerline_box.panel import controller


class RecordingTimer:
    """threading.Timer test double: start() queues the call instead of firing it."""

    pending = []

    def __init__(self, interval, function):
        self.interval = interval
        self.function = function

    def start(self):
        RecordingTimer.pending.append(self)

    def cancel(self):
        if self in RecordingTimer.pending:
            RecordingTimer.pending.remove(self)


def run_next_timer():
    """Simulate the oldest scheduled Timer firing."""
    timer = RecordingTimer.pending.pop(0)
    timer.function()


@pytest.fixture(autouse=True)
def reset_controller_state(monkeypatch):
    """Reset controller runtime state and stub out GUI/UART side effects for every test."""
    RecordingTimer.pending.clear()
    monkeypatch.setattr(controller, "Timer", RecordingTimer)

    controller._controller.state = controller.panel_state['normal']
    controller._controller.event = None
    controller._controller.event_timer = None
    controller._controller.current_button = {'id': None, 'bg': '#000000', 'fg': '#000000'}
    controller._controller.previous_button = {'id': None, 'bg': '#000000', 'fg': '#000000'}
    controller._controller.double_command = None
    controller._controller.double_command_comment = None

    monkeypatch.setattr(controller.power_line, "is_connected", lambda: True)
    monkeypatch.setattr(controller.power_line, "send", lambda data: data)
    monkeypatch.setattr(controller.terminal_main, "add_text", lambda *a, **k: None)

    button_configs = []
    monkeypatch.setattr(controller.gui, "config_button", lambda button_id, **kwargs: button_configs.append((button_id, kwargs)))

    yield button_configs


def run_all_pending_timers():
    while RecordingTimer.pending:
        run_next_timer()


def test_init_sequence_sends_expected_commands(monkeypatch, reset_controller_state):
    button_configs = reset_controller_state
    monkeypatch.setattr(controller.gui, "get_button_data", lambda button_id, text=None: "INIT")

    sent = []
    monkeypatch.setattr(controller.power_line, "send", lambda data: sent.append(data.decode('utf-8').strip()) or data)

    controller.init("panel_main_init")
    run_all_pending_timers()

    assert sent == ["safepwr 0", "pwr 0", "safepwr 1", "init 1000"]
    button_texts = [kwargs.get("text") for _, kwargs in button_configs]
    assert button_texts == ["INIT in progress", "INIT"]


def test_dpc_sequence_sends_expected_commands(monkeypatch, reset_controller_state):
    button_configs = reset_controller_state
    monkeypatch.setattr(controller.gui, "get_button_data", lambda button_id, text=None: "DPC")

    sent = []
    monkeypatch.setattr(controller.power_line, "send", lambda data: sent.append(data.decode('utf-8').strip()) or data)

    controller.dpc("panel_dpc")
    run_all_pending_timers()

    assert sent == ["pwr 0", "safepwr 1", "pwr 1", "pwr 0", "pwr 1", "pwr 0", "pwr 1"]
    button_texts = [kwargs.get("text") for _, kwargs in button_configs]
    assert button_texts == ["DPC in progress", "DPC"]


def test_init_does_not_start_a_second_sequence_while_one_is_running(monkeypatch, reset_controller_state):
    monkeypatch.setattr(controller.gui, "get_button_data", lambda button_id, text=None: "INIT")

    started_first = controller.create_event(new_event=controller.events_list['init_0'], time=0)
    started_second = controller.create_event(new_event=controller.events_list['init_0'], time=0)

    assert started_first is True
    assert started_second is None
