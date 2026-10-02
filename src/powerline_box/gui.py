
import tkinter as tk
import re

Buttons = {}  # Buttons   -      button_id -> {"frame", "button"}
Labels = []   # Labels    -      {"label_id", "text", "label"} (ids intentionally reused, kept as a list)
Texts = {}    # Texts     -      text_id -> {"text", "readonly"}
Entries = {}  # Entries   -      entry_id -> {"frame", "entry"}
Listboxes = {}   # Listboxes -   listbox_id -> {"frame", "listbox"}
Dropdowns = {}   # Dropdowns -   dropdown_id -> {"frame", "variable", "menu"}

_root = None  # Tk root window, registered via set_root() once created


def set_root(root):
    """Register the Tk root window so background threads can marshal calls onto the main thread.
    --------------------------------------------------------------------------------------------------------------------
    """
    global _root
    _root = root


def run_on_ui_thread(func):
    """Schedule func to run on the Tk main thread (Tkinter widgets are not thread-safe).
    --------------------------------------------------------------------------------------------------------------------
    """
    if _root is not None:
        _root.after(0, func)
    else:
        func()


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

    new_button = {"frame": frame_button, "button": button}

    if button_id is not None:
        Buttons[button_id] = new_button


def config_button(button_id, text=None, height=None, width=None, x=None, y=None, action=None, relx=None, rely=None,
                  bg=None, fg=None, active_background=None, active_foreground=None):
    """Config button:
    based on id (ID is assigned with create_button function
    --------------------------------------------------------------------------------------------------------------------
    """

    # find the button
    record = Buttons.get(button_id)

    # return error in case when button will not be find
    if record is None:
        return "button not found"
    button = record["button"]
    frame = record["frame"]

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
    record = Buttons.get(button_id)

    if record is None:
        # return error in case when button will not be find
        return "button not found"
    else:
        button = record["button"]
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
    record = Buttons.get(button_id)

    # return error in case when button will not be find
    if record is None:
        return "button not found"

    record["button"].pack_forget()

    # in case of success return 1
    return 1


def show_button(button_id):
    """button_id:
    based on id (ID is assigned with create_button function
    --------------------------------------------------------------------------------------------------------------------
    """

    # find the button
    record = Buttons.get(button_id)

    # return error in case when button will not be find
    if record is None:
        return "button not found"

    record["button"].pack(fill=tk.BOTH, expand=1)

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

    if readonly:
        text.config(state=tk.DISABLED)
    else:
        text.config(state=tk.NORMAL)

    Texts[text_id] = {"text": text, "readonly": readonly}


def add_text(text_id, new_text):
    """add text
    --------------------------------------------------------------------------------------------------------------------
    """
    record = Texts.get(text_id)
    if record is None:
        return

    text = record["text"]
    if record["readonly"]:
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
    record = Texts.get(text_id)
    if record is None:
        return

    text = record["text"]
    if record["readonly"]:
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

    if readonly:
        entry.config(state=tk.DISABLED)
    else:
        entry.config(state=tk.NORMAL)
    
    Entries[entry_id] = {"frame": frame_entry, "entry": entry}
    

def config_entry(entry_id, x=None, y=None, text=None, height=None, width=None, readonly=None):
    """config_entry
    --------------------------------------------------------------------------------------------------------------------
    """
    # find the entry
    record = Entries.get(entry_id)

    # return error in case when button will not be find
    if record is None:
        return "entry not found"
    entry = record["entry"]
    frame = record["frame"]

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
        if readonly:
            entry.config(state=tk.DISABLED)
        else:
            entry.config(state=tk.NORMAL)


def get_entry(entry_id):
    """get entry
    --------------------------------------------------------------------------------------------------------------------
    """
    record = Entries.get(entry_id)
    return record["entry"] if record is not None else None


def create_listbox(frame, listbox_id, x, y, width, height, multiple=False):
    """create listbox
    A plain tk.Listbox with a vertical scrollbar; multiple=True allows multi-selection
    (used by the automation editor to group steps into a loop).
    --------------------------------------------------------------------------------------------------------------------
    """
    frame_listbox = tk.Frame(frame, height=height, width=width)
    frame_listbox.pack_propagate(0)
    frame_listbox.place(x=x, y=y)

    scrollbar = tk.Scrollbar(frame_listbox)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(frame_listbox, font=("Consolas", 10),
                        selectmode=tk.EXTENDED if multiple else tk.BROWSE,
                        yscrollcommand=scrollbar.set)
    listbox.pack(fill=tk.BOTH, expand=1)
    scrollbar.config(command=listbox.yview)

    Listboxes[listbox_id] = {"frame": frame_listbox, "listbox": listbox}


def set_listbox_items(listbox_id, items):
    """set listbox items
    Replaces the listbox's contents with `items` (a list of display strings).
    --------------------------------------------------------------------------------------------------------------------
    """
    record = Listboxes.get(listbox_id)
    if record is None:
        return
    listbox = record["listbox"]
    listbox.delete(0, tk.END)
    for item in items:
        listbox.insert(tk.END, item)


def get_listbox_selection(listbox_id):
    """get listbox selection
    Returns the list of selected indices (empty list if none/not found).
    --------------------------------------------------------------------------------------------------------------------
    """
    record = Listboxes.get(listbox_id)
    if record is None:
        return []
    return list(record["listbox"].curselection())


def bind_listbox_select(listbox_id, action):
    """bind listbox select
    --------------------------------------------------------------------------------------------------------------------
    """
    record = Listboxes.get(listbox_id)
    if record is None:
        return
    record["listbox"].bind("<<ListboxSelect>>", lambda event: action())


def create_dropdown(frame, dropdown_id, values, x, y, width, height=25, default=None):
    """create dropdown
    A plain tk.OptionMenu backed by a StringVar (used to pick an existing panel
    button as the source of a Command step). The frame uses pack_propagate(0) so
    `width`/`height` are pixels, same as create_entry/create_listbox - OptionMenu's
    own `width` option is in character units, so it's intentionally left unset here.
    --------------------------------------------------------------------------------------------------------------------
    """
    variable = tk.StringVar(frame)
    variable.set(default if default is not None else (values[0] if values else ""))

    frame_dropdown = tk.Frame(frame, height=height, width=width)
    frame_dropdown.pack_propagate(0)
    frame_dropdown.place(x=x, y=y)

    menu = tk.OptionMenu(frame_dropdown, variable, *values) if values else tk.OptionMenu(frame_dropdown, variable, "")
    menu.pack(fill=tk.BOTH, expand=1)

    Dropdowns[dropdown_id] = {"frame": frame_dropdown, "variable": variable, "menu": menu}


def set_dropdown_values(dropdown_id, values, default=None):
    """set dropdown values
    Replaces the dropdown's choices (used when the panel buttons list changes).
    --------------------------------------------------------------------------------------------------------------------
    """
    record = Dropdowns.get(dropdown_id)
    if record is None:
        return
    variable = record["variable"]
    menu = record["menu"]["menu"]
    menu.delete(0, tk.END)
    for value in values:
        menu.add_command(label=value, command=lambda v=value: variable.set(v))
    variable.set(default if default is not None else (values[0] if values else ""))


def get_dropdown_value(dropdown_id):
    """get dropdown value
    --------------------------------------------------------------------------------------------------------------------
    """
    record = Dropdowns.get(dropdown_id)
    return record["variable"].get() if record is not None else None


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
