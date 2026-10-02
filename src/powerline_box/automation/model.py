"""Data model for automation scripts: plain-dict steps/scripts plus validation helpers.

A script is a plain dict:
    {"name": str, "repeat": int, "steps": [step, ...]}
`repeat` is how many times the whole script runs; 0 means "until stopped".

A step is a plain dict with a "type" key:
    - {"type": "command", "name": str, "command": str}
    - {"type": "wait", "delay_ms": int}
    - {"type": "loop", "repeat": int, "steps": [command/wait step, ...]}  (no nested loops)
    - {"type": "preset", "name": str, "steps": [command/wait step, ...]}
      a fixed hardware sequence (Init/Power On/Power Off/DPC) - shown collapsed
      (just its name) in the editor, expanded when run.
    - {"type": "script", "name": str, "steps": [step, ...]}
      a copy of another saved script's steps, inserted inline - shown expanded
      (name + indented steps) in the editor.
----------------------------------------------------------------------------------------------------------------
"""

STEP_COMMAND = "command"
STEP_WAIT = "wait"
STEP_LOOP = "loop"
STEP_PRESET = "preset"
STEP_SCRIPT = "script"

WAIT_MIN_MS = 1
WAIT_MAX_MS = 60_000
LOOP_MIN_REPEAT = 1
LOOP_MAX_REPEAT = 999
SCRIPT_REPEAT_FOREVER = 0


def new_command_step(name, command):
    """new_command_step
    ----------------------------------------------------------------------------------------------------------------
    """
    return {"type": STEP_COMMAND, "name": name, "command": command}


def new_wait_step(delay_ms):
    """new_wait_step
    ----------------------------------------------------------------------------------------------------------------
    """
    return {"type": STEP_WAIT, "delay_ms": int(delay_ms)}


def new_loop_step(repeat, steps=None):
    """new_loop_step
    ----------------------------------------------------------------------------------------------------------------
    """
    return {"type": STEP_LOOP, "repeat": int(repeat), "steps": list(steps) if steps else []}


def new_preset_step(name, steps):
    """new_preset_step
    ----------------------------------------------------------------------------------------------------------------
    """
    return {"type": STEP_PRESET, "name": name, "steps": list(steps)}


def new_script_step(name, steps):
    """new_script_step
    ----------------------------------------------------------------------------------------------------------------
    """
    return {"type": STEP_SCRIPT, "name": name, "steps": list(steps)}


def new_script(name, repeat=SCRIPT_REPEAT_FOREVER, steps=None):
    """new_script
    ----------------------------------------------------------------------------------------------------------------
    """
    return {"name": name, "repeat": int(repeat), "steps": list(steps) if steps else []}


def validate_step(step, allow_container=True):
    """validate_step
    Returns True if step is well-formed, False otherwise. allow_container gates the
    container types (loop/preset/script): a loop's own body is command/wait only, so
    it's validated with allow_container=False; everywhere else all types are allowed.
    ----------------------------------------------------------------------------------------------------------------
    """
    if not isinstance(step, dict):
        return False
    step_type = step.get("type")

    if step_type == STEP_COMMAND:
        name = step.get("name")
        command = step.get("command")
        return isinstance(name, str) and isinstance(command, str) and command != ""

    if step_type == STEP_WAIT:
        delay = step.get("delay_ms")
        return isinstance(delay, int) and not isinstance(delay, bool) and WAIT_MIN_MS <= delay <= WAIT_MAX_MS

    if step_type == STEP_LOOP and allow_container:
        repeat = step.get("repeat")
        if not (isinstance(repeat, int) and not isinstance(repeat, bool) and LOOP_MIN_REPEAT <= repeat <= LOOP_MAX_REPEAT):
            return False
        inner_steps = step.get("steps")
        # loops can't be nested: inner steps are command/wait only
        return isinstance(inner_steps, list) and len(inner_steps) > 0 and all(
            validate_step(inner, allow_container=False) for inner in inner_steps
        )

    if step_type in (STEP_PRESET, STEP_SCRIPT) and allow_container:
        name = step.get("name")
        inner_steps = step.get("steps")
        if not (isinstance(name, str) and name != ""):
            return False
        return isinstance(inner_steps, list) and len(inner_steps) > 0 and all(
            validate_step(inner, allow_container=True) for inner in inner_steps
        )

    return False


def validate_steps(steps):
    """validate_steps
    Returns True if steps is a non-empty list of well-formed steps. Used when running
    an unsaved/ad-hoc script - a name is only required for saving, not for running.
    ----------------------------------------------------------------------------------------------------------------
    """
    return isinstance(steps, list) and len(steps) > 0 and all(validate_step(step) for step in steps)


def validate_script(script):
    """validate_script
    Returns True if script is well-formed (name + valid steps list), False otherwise.
    ----------------------------------------------------------------------------------------------------------------
    """
    if not isinstance(script, dict):
        return False
    if not isinstance(script.get("name"), str) or script["name"] == "":
        return False

    repeat = script.get("repeat")
    if not (isinstance(repeat, int) and not isinstance(repeat, bool) and repeat >= SCRIPT_REPEAT_FOREVER):
        return False

    steps = script.get("steps")
    return isinstance(steps, list) and all(validate_step(step) for step in steps)


def flatten_steps(steps):
    """flatten_steps
    Expands loop steps into a flat list of command/wait steps (loop bodies repeated in place).
    Does not expand the outer script-level repeat - the runner handles that separately.
    ----------------------------------------------------------------------------------------------------------------
    """
    flat = []
    for step in steps:
        if step["type"] == STEP_LOOP:
            for _ in range(step["repeat"]):
                flat.extend(flatten_steps(step["steps"]))
        elif step["type"] in (STEP_PRESET, STEP_SCRIPT):
            flat.extend(flatten_steps(step["steps"]))
        else:
            flat.append(step)
    return flat
