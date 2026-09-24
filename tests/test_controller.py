from powerline_box.panel.controller import classify_ppc_command


def test_classify_single_frame_command():
    kind, parts = classify_ppc_command("ppc d0f")
    assert kind == "single"
    assert parts == ("ppc d0f",)


def test_classify_double_frame_command_splits_in_two():
    # real example from config/panel_buttons.json
    kind, parts = classify_ppc_command("ppc d11fd00f")
    assert kind == "double"
    cmd1, cmd2 = parts
    assert cmd1 == "ppc d11f"
    assert cmd2 == "ppc d00f"


def test_classify_other_command_is_passed_through():
    kind, parts = classify_ppc_command("pwr 1")
    assert kind == "other"
    assert parts == ("pwr 1",)


def test_classify_init_command_is_other():
    kind, parts = classify_ppc_command("init 1000")
    assert kind == "other"
    assert parts == ("init 1000",)
