
import uart.terminal as terminal
import gui_terminal.terminal_main as terminal_main


power_line_terminal = {
    'id': "PL",
    'connected': False
}


def connect(port="COM4", baud=9600):
    """connect
    --------------------------------------------------------------------------------------------------------------------
    """
    state, message = terminal.connect(terminal_id=power_line_terminal['id'], port=port, baud=9600, callback=callback)
    return state


def disconnect():
    """disconnect
    --------------------------------------------------------------------------------------------------------------------
    """
    state, error = terminal.disconnect(terminal_id=power_line_terminal['id'])
    return state


def is_connected():
    """is_connected
    --------------------------------------------------------------------------------------------------------------------
    """
    return terminal.is_open(terminal_id=power_line_terminal['id'])


def callback(message):
    """callback
    --------------------------------------------------------------------------------------------------------------------
    """
    message = (message.decode('utf-8')).replace('\r\n', '')
    if message is not "":
        terminal_main.add_text(message, received=True)


def send(message):
    """send
    --------------------------------------------------------------------------------------------------------------------
    """
    if is_connected() is True:
        terminal.send_data(terminal_id=power_line_terminal['id'], data=message)
        return message
    else:
        return "not connected".encode('utf-8')
