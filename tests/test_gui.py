from powerline_box import gui


def test_check_color_accepts_short_hex():
    assert gui.check_color("#fff") is True


def test_check_color_accepts_long_hex():
    assert gui.check_color("#1C6A8E") is True


def test_check_color_rejects_missing_hash():
    result = gui.check_color("1C6A8E")
    assert result != True
    assert "not a valid hex color code" in result


def test_check_color_rejects_wrong_length():
    result = gui.check_color("#12345")
    assert result != True
    assert "not a valid hex color code" in result


def test_check_color_rejects_non_hex_chars():
    result = gui.check_color("#GGGGGG")
    assert result != True
    assert "not a valid hex color code" in result


def test_button_registry_lookup_by_id():
    gui.Buttons.clear()
    gui.Buttons["some_id"] = {"frame": object(), "button": object()}

    assert gui.config_button(button_id="unknown_id") == "button not found"
    assert gui.hide_button(button_id="unknown_id") == "button not found"
