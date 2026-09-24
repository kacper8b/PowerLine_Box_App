import datetime

from powerline_box import config
from powerline_box import gui

# USED interfaces:
id_text = {
    'terminal': "terminal_1",
}


def create_terminal(frame, height, width, x, y, readonly):
    """create terminal
    --------------------------------------------------------------------------------------------------------------------
    """
    gui.create_text(text_id=id_text['terminal'], frame=frame, height=height, width=width, x=x, y=y, readonly=readonly)


def add_text(text, received=False):
    """add text
    --------------------------------------------------------------------------------------------------------------------
    """

    now = datetime.datetime.now()
    time = str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + ":" + str(now.second).zfill(2)

    count = text.count('')
    column_max = config.terminal['column_max']+1
    rows = int(count / column_max) + (count % column_max > 0)
    new_text = ""
    current_char = 0

    if received is True:
        message_type_char = "<--"
    else:
        message_type_char = "-->"

    for i in range(rows):
        if i == 0:
            # time + text
            new_text = "{0}:\t{1}\t{2}".format(time, message_type_char, text[0:column_max-1])
            current_char = column_max
        else:
            # remaining part of text
            new_text += "\n\t{0}\t{1}".format(message_type_char, text[current_char:current_char+column_max-1])
            current_char = current_char+column_max-1

    gui.add_text(text_id=id_text['terminal'], new_text=new_text)


def clear():
    """clear terminal
    --------------------------------------------------------------------------------------------------------------------
    """
    gui.remove_text(text_id=id_text['terminal'])
