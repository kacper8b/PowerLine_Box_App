"""Tests for the automation script execution engine in automation/runner.py.

Like test_controller_sequences.py, threading.Timer is replaced with a test double
that records pending calls instead of firing them; tests manually advance the
sequence by calling run_next_timer() once per scheduled step.
"""
import pytest

from powerline_box.automation import model
from powerline_box.automation import runner
from powerline_box.panel import controller as panel


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
def reset_state(monkeypatch):
    """Reset panel/runner state and stub out GUI/UART side effects for every test."""
    RecordingTimer.pending.clear()
    monkeypatch.setattr(runner, "Timer", RecordingTimer)
    monkeypatch.setattr(runner.gui, "run_on_ui_thread", lambda func: func())
    monkeypatch.setattr(runner.power_line, "is_connected", lambda: True)
    monkeypatch.setattr(runner.power_line, "send", lambda data: data)
    monkeypatch.setattr(runner.terminal_main, "add_text", lambda *a, **k: None)

    panel._controller.state = panel.panel_state['normal']
    panel._controller.event = None
    panel._controller.event_timer = None


def test_run_rejects_when_not_connected(monkeypatch):
    monkeypatch.setattr(runner.power_line, "is_connected", lambda: False)
    script = model.new_script("test", steps=[model.new_wait_step(500)])
    assert runner.run(script) is False
    assert not runner.is_running()


def test_run_rejects_invalid_script():
    assert runner.run({"name": "", "repeat": 0, "steps": []}) is False


def test_run_allows_unnamed_ad_hoc_script():
    # a name is only required to *save* a script, not to run it
    script = model.new_script(name="", steps=[model.new_wait_step(500)])
    assert runner.run(script) is True


def test_run_rejects_when_panel_event_in_progress():
    panel._controller.event = panel.events_list['init_0']
    script = model.new_script("test", steps=[model.new_wait_step(500)])
    assert runner.run(script) is False


def test_run_blocked_while_already_running():
    script = model.new_script("test", steps=[model.new_wait_step(500)])
    assert runner.run(script) is True
    assert runner.run(script) is False


def test_run_executes_steps_in_order_and_completes():
    executed = []
    finished = []
    script = model.new_script("test", repeat=1, steps=[
        model.new_command_step("Up", "ppc d0f"),
        model.new_wait_step(500),
        model.new_command_step("Stop", "ppc df"),
    ])

    assert runner.run(script, on_step=lambda i, s: executed.append(s['type']),
                      on_finished=lambda r: finished.append(r)) is True
    assert executed == ["command"]
    assert panel.is_automation_running()

    run_next_timer()
    assert executed == ["command", "wait"]

    run_next_timer()
    assert executed == ["command", "wait", "command"]
    assert runner.is_running()

    run_next_timer()
    assert finished == ["completed"]
    assert not runner.is_running()
    assert not panel.is_automation_running()


def test_repeat_forever_loops_until_stopped():
    script = model.new_script("test", repeat=0, steps=[model.new_wait_step(100)])
    executed = []
    assert runner.run(script, on_step=lambda i, s: executed.append(i)) is True
    for _ in range(5):
        run_next_timer()
    assert len(executed) == 6
    assert runner.is_running()
    runner.stop()
    assert not runner.is_running()


def test_stop_cancels_pending_timer_and_resets_state():
    script = model.new_script("test", repeat=0, steps=[model.new_wait_step(500)])
    finished = []
    assert runner.run(script, on_finished=lambda r: finished.append(r)) is True
    assert RecordingTimer.pending

    runner.stop()
    assert finished == ["stopped"]
    assert not runner.is_running()
    assert not RecordingTimer.pending
