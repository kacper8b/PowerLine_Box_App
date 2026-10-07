from powerline_box.automation import model


def test_new_command_step():
    assert model.new_command_step("Up", "ppc d0f") == {"type": "command", "name": "Up", "command": "ppc d0f"}


def test_validate_command_step():
    assert model.validate_step(model.new_command_step("Up", "ppc d0f"))
    assert not model.validate_step(model.new_command_step("Up", ""))


def test_validate_wait_step():
    assert model.validate_step(model.new_wait_step(500))
    assert not model.validate_step(model.new_wait_step(0))
    assert not model.validate_step(model.new_wait_step(model.WAIT_MAX_MS + 1))


def test_validate_loop_step():
    loop = model.new_loop_step(3, [model.new_command_step("Up", "ppc d0f"), model.new_wait_step(500)])
    assert model.validate_step(loop)
    assert not model.validate_step(model.new_loop_step(0, [model.new_wait_step(500)]))
    assert not model.validate_step(model.new_loop_step(2, []))


def test_loop_cannot_be_nested():
    inner_loop = model.new_loop_step(2, [model.new_wait_step(500)])
    outer_loop = model.new_loop_step(2, [inner_loop])
    assert not model.validate_step(outer_loop)


def test_validate_steps_requires_at_least_one_step():
    assert model.validate_steps([model.new_wait_step(500)])
    assert not model.validate_steps([])
    assert not model.validate_steps([model.new_wait_step(0)])


def test_validate_script():
    script = model.new_script("test", repeat=0, steps=[model.new_wait_step(500)])
    assert model.validate_script(script)
    assert not model.validate_script(model.new_script("", steps=[model.new_wait_step(500)]))
    assert not model.validate_script({"name": "x", "repeat": -1, "steps": []})


def test_flatten_steps_expands_loop():
    steps = [
        model.new_command_step("Up", "ppc d0f"),
        model.new_loop_step(2, [model.new_wait_step(500), model.new_command_step("Stop", "ppc df")]),
    ]
    assert model.flatten_steps(steps) == [
        model.new_command_step("Up", "ppc d0f"),
        model.new_wait_step(500),
        model.new_command_step("Stop", "ppc df"),
        model.new_wait_step(500),
        model.new_command_step("Stop", "ppc df"),
    ]


def test_validate_preset_step():
    preset = model.new_preset_step("Init", [model.new_command_step("safepwr 0", "safepwr 0"), model.new_wait_step(500)])
    assert model.validate_step(preset)
    assert not model.validate_step(model.new_preset_step("", [model.new_wait_step(500)]))
    assert not model.validate_step(model.new_preset_step("Init", []))


def test_validate_script_step_allows_loop_inside():
    script_step = model.new_script_step("tests", [
        model.new_command_step("Up", "ppc d0f"),
        model.new_loop_step(2, [model.new_command_step("Up", "ppc d0f")]),
    ])
    assert model.validate_step(script_step)


def test_flatten_steps_expands_preset_and_script():
    preset = model.new_preset_step("Init", [model.new_command_step("safepwr 0", "safepwr 0"), model.new_wait_step(500)])
    script_step = model.new_script_step("tests", [model.new_command_step("Up", "ppc d0f")])
    assert model.flatten_steps([preset, script_step]) == [
        model.new_command_step("safepwr 0", "safepwr 0"),
        model.new_wait_step(500),
        model.new_command_step("Up", "ppc d0f"),
    ]
