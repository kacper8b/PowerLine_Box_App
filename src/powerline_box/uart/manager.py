import logging

from powerline_box import terminal_log as terminal_main
from powerline_box.uart.serial_port import Uart

logger = logging.getLogger(__name__)

Uart1 = Uart()
Uart2 = Uart()
Uart3 = Uart()
Uart4 = Uart()

terminals = [{"number": 1, "state": "not used", "terminal_id": 0, "terminal": Uart1},
             {"number": 2, "state": "not used", "terminal_id": 0, "terminal": Uart2},
             {"number": 3, "state": "not used", "terminal_id": 0, "terminal": Uart3},
             {"number": 4, "state": "not used", "terminal_id": 0, "terminal": Uart4}]


def connect(terminal_id, callback, port=None, baud=None):
    """connect
    --------------------------------------------------------------------------------------------------------------------
    """

    state = False
    selected_terminal = None
    terminal = None
    message = None

    for t in terminals:
        if t["state"] == "not used":
            selected_terminal = t
            break

    if selected_terminal is None:
        message = "there is no free terminal to use"
    else:
        state = selected_terminal["terminal"].connect(port=port, baud=baud)

    if state:
        message = "connected"
        selected_terminal["state"] = "connect"
        selected_terminal["terminal_id"] = terminal_id
        selected_terminal["terminal"].register_new_thread(callback)
    else:
        message = "Not possible to connect with Port: {0}".format(port)

    if state:
        logger.info(message)
    else:
        logger.warning(message)
    terminal_main.add_text(message)
    return state, message


def disconnect(terminal_id):
    """disconnect
    --------------------------------------------------------------------------------------------------------------------
    """

    selected_terminal = None
    state = False
    error = None

    for terminal in terminals:
        if terminal_id == terminal["terminal_id"]:
            selected_terminal = terminal

    if selected_terminal is None:
        error = "can't disconnect, terminal not found"
    else:
        state = selected_terminal["terminal"].disconnect()

    if state:
        error = "Disconnected"
        selected_terminal["state"] = "not used"
        selected_terminal["terminal_id"] = 0
    else:
        error = "Error, not connected"

    if state:
        logger.info(error)
    else:
        logger.warning(error)
    terminal_main.add_text(error)

    return state, error


def send_data(terminal_id, data=' '):
    """send_data
    --------------------------------------------------------------------------------------------------------------------
    """

    for terminal in terminals:
        if terminal_id == terminal["terminal_id"]:
            terminal["terminal"].send_data(data)


def is_open(terminal_id):
    """is_open
    --------------------------------------------------------------------------------------------------------------------
    """

    for terminal in terminals:
        if terminal_id == terminal["terminal_id"]:
            return terminal["terminal"].is_open()
    return False
