import tkinter as tk
import re

Buttons = []  # Buttons   -      {"button_id", "frame", "button"}
Labels = []   # Labels    -      {"label_id", "text", "label"}
Texts = []    # Texts     -      {"text_id", "frame", "text", "readonly"}
Entries = []  # Entries   -      {"entry_id", "frame", "entry"} 


def create_button(frame, button_id=None, text=" ", height=30, width=120, x=0, y=0, action=None, relx=None, rely=None,
                  bg=None, fg=None, active_background=None, active_foreground=None):
    """Create new button
    if the button_id will not be given the button can't be modified later
    --------------------------------------------------------------------------------------------------------------------
    """

    frame_button = tk.Frame(frame, height=height, width=width)
    frame_button.pack_propagate(0)
    frame_button.place(x=x, y=y)
    frame_button.place(anchor="center")
    frame_button['bg'] = frame_button.master['bg']

    if relx is not None:
        frame_button.place(relx=relx)
    if rely is not None:
        frame_button.place(rely=rely)

    # create button
    button = tk.Button(frame_button, text=text)
    button.pack(fill=tk.BOTH, expand=1)

    # config button
    if action is not None:
        button.config(command=lambda variable=id: action())
    if bg is not None:
        button.config(bg=bg)
    if fg is not None:
        button.config(fg=fg)
    if active_background is not None:
        button.config(activebackground=active_background)
    if active_foreground is not None:
        button.config(activeforeground=active_foreground)

    new_button = {"button_id": button_id, "frame": frame_button, "button": button}

    if button_id is not None:
        Buttons.append(new_button)


def config_button(button_id, text=None, height=None, width=None, x=None, y=None, action=None, relx=None, rely=None,
                  bg=None, fg=None, active_background=None, active_foreground=None):
    """Config button:
    based on id (ID is assigned with create_button function
    --------------------------------------------------------------------------------------------------------------------
    """

    # find the button
    button = None
    frame = None
    for b in Buttons:
        if b["button_id"] == button_id:
            button = b["button"]
            frame = b["frame"]
            break

    # return error in case when button will not be find
    if button is None:
        return "button nof found"

    # configuration
    if text is not None:
        button.config(text=text)
    if height is not None:
        frame.config(height=height)
    if width is not None:
        frame.config(width=width)
    if x is not None:
        frame.place(x=x)
    if y is not None:
        frame.place(y=y)
    if action is not None:
        button.config(command=lambda: action())
    if relx is not None:
        frame.place(relx=relx)
    if rely is not None:
        frame.place(rely=rely)
    if bg is not None:
        button.config(bg=bg)
    if fg is not None:
        button.config(fg=fg)
    if active_background is not None:
        button.config(activebackground=active_background)
    if active_foreground is not None:
        button.config(activeforeground=active_foreground)

    # in case of success return 1
    return 1


def get_button_data(button_id, text=None, bg=None, fg=None, x=None, y=None):
    """get_button_text
    based on id (ID is assigned with create_button function
    --------------------------------------------------------------------------------------------------------------------
    """

    # find the button
    button = None
    for b in Buttons:
        if b["button_id"] == button_id:
            button = b["button"]
            break

    if button is None:
        # return error in case when button will not be find
        return "button nof found"
    else:
        if text is not None:
            return button['text']
        if bg is not None:
            return button['bg']
        if fg is not None:
            return button['fg']
        if x is not None:
            return button['x']
        if y is not None:
            return button['y']


def hide_button(button_id):
    """button_id:
    based on id (ID is assigned with create_button function
    --------------------------------------------------------------------------------------------------------------------
    """

    # find the button
    button = None
    for b in Buttons:
        if b["button_id"] == button_id:
            button = b["button"]
            frame = b["frame"]
            break

    # return error in case when button will not be find
    if button is None:
        return "button nof found"

    button.pack_forget()

    # in case of success return 1
    return 1


def show_button(button_id):
    """button_id:
    based on id (ID is assigned with create_button function
    --------------------------------------------------------------------------------------------------------------------
    """

    # find the button
    button = None
    for b in Buttons:
        if b["button_id"] == button_id:
            button = b["button"]
            frame = b["frame"]
            break

    # return error in case when button will not be find
    if button is None:
        return "button nof found"

    button.pack(fill=tk.BOTH, expand=1)

    # in case of success return 1
    return 1


def create_label(frame, label_id=None, text="", x=None, y=None):
    """create label
    --------------------------------------------------------------------------------------------------------------------
    """

    label = tk.Label(frame, text=text)

    if x is not None:
        label.place(x=x)
    if y is not None:
        label.place(y=y)

    label['bg'] = label.master['bg']

    new_label = {"label_id": label_id, "text": text, "label": label}
    Labels.append(new_label)


def config_label(label_id, x, y, text=""):
    """config label
    --------------------------------------------------------------------------------------------------------------------
    """

    # find the label
    label = None
    for l in Labels:
        if l["label_id"] == label_id:
            label = l["label"]
            break

    # return error in case when label will not be find
    if label is None:
        return "label nof found"

    if text is not None:
        label.config(text=text)
    if x is not None:
        label.place(x=x)
    if y is not None:
        label.place(y=y)

    # in case of success return 1
    return 1


def create_text(frame, height, width, x, y, text_id=None, readonly=True, background=None):
    """create text
    --------------------------------------------------------------------------------------------------------------------
    """

    frame_text = tk.Frame(frame, height=height, width=width)
    frame_text.pack_propagate(0)

    if x is not None:
        frame_text.place(x=x)
    if y is not None:
        frame_text.place(y=y)

    text = tk.Text(frame_text, font=("Consolas", 10))
    text.pack(fill=tk.BOTH, expand=1)

    if background is not None:
        text.config(background=background)

    if readonly is True:
        text.config(state=tk.DISABLED)
    else:
        text.config(state=tk.NORMAL)

    new_text = {"text_id": text_id, "text": text, "readonly": readonly}
    Texts.append(new_text)


def get_text(text_id):
    """get text
    --------------------------------------------------------------------------------------------------------------------
    """
    for t in Texts:
        if t["text_id"] == text_id:
            return t["text"]


def add_text(text_id, new_text):
    """add text
    --------------------------------------------------------------------------------------------------------------------
    """
    readonly = None
    text = None

    # find the Text object, text
    for t in Texts:
        if t["text_id"] == text_id:
            readonly = t["readonly"]
            text = t["text"]
            break

    if readonly is True:
        text.config(state=tk.NORMAL)
        text.insert(tk.END, "{0}\n".format(new_text))
        text.config(state=tk.DISABLED)
        text.see(tk.END)
    else:
        text.insert(tk.END, "{0}\n".format(new_text))
        text.see(tk.END)


def remove_text(text_id):
    """remove_text
    --------------------------------------------------------------------------------------------------------------------
    """
    readonly = None
    text = None

    # find the Text object, text
    for t in Texts:
        if t["text_id"] == text_id:
            readonly = t["readonly"]
            text = t["text"]
            break

    if readonly is True:
        text.config(state=tk.NORMAL)
        text.delete("1.0", tk.END)
        text.config(state=tk.DISABLED)
    else:
        text.delete("1.0", tk.END)


def create_entry(frame, entry_id, x, y, text=None, height=30, width=200, readonly=False):
    """create entry
    --------------------------------------------------------------------------------------------------------------------
    """
    
    frame_entry = tk.Frame(frame, height=height, width=width)
    frame_entry.pack_propagate(0)
    
    if x is not None:
        frame_entry.place(x=x)
    if y is not None:
        frame_entry.place(y=y)

    frame_entry.place(anchor="w")

    entry = tk.Entry(frame_entry, font=("Consolas", 12))
    entry.pack(fill=tk.BOTH, expand=1)

    if text is not None:
        entry.delete(0, "end")
        entry.insert(0, text)

    if readonly is True:
        entry.config(state=tk.DISABLED)
    else:
        entry.config(state=tk.NORMAL)
    
    new_entry = {"entry_id": entry_id, "frame": frame_entry, "entry": entry}
    Entries.append(new_entry)
    

def config_entry(entry_id, x=None, y=None, text=None, height=None, width=None, readonly=None):
    """config_entry
    --------------------------------------------------------------------------------------------------------------------
    """
    # find the entry
    entry = None
    frame = None
    for e in Entries:
        if e["entry_id"] == entry_id:
            entry = e["entry"]
            frame = e["frame"]
            break

    # return error in case when button will not be find
    if entry is None:
        return "entry nof found"

    if x is not None:
        frame.place(x=x)
    if y is not None:
        frame.place(y=y)

    if height is not None:
        frame.config(height=height)
    if width is not None:
        frame.config(width=width)

    if text is not None:
        entry.delete(0, "end")
        entry.insert(0, text)

    if readonly is not None:
        if readonly is True:
            entry.config(state=tk.DISABLED)
        else:
            entry.config(state=tk.NORMAL)


def get_entry(entry_id):
    """get entry
    --------------------------------------------------------------------------------------------------------------------
    """
    for e in Entries:
        if e["entry_id"] == entry_id:
            return e["entry"]


def check_color(color_code):
    """
    Check the validity of the hexadecimal code of various node and edge color
    related attributes.

    This function returns an error if the hexadecimal code is not of the format
    '#XXX' or '#XXXXXX', i.e. hexadecimal color code is not valid.

    :param color_code: color code
    """
    # if color name is given instead of hex code, no need to check its validity
    if not color_code.startswith('#'):
        return color_code + ' is not a valid hex color code.'
    valid = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color_code)
    if valid is None:
        return color_code + ' is not a valid hex color code.'
    else:
        return True
