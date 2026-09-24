import json
import tkinter as tk

from powerline_box import config
from powerline_box import gui
from powerline_box.uart import power_line


# USED interfaces:
id_button = {
    'connect': "connect",
}

id_entry = {
    'COM': "PowerLine_COM",
    'baud rate': "PowerLine_baud",
}

PL_terminal = {
    'id': "PL",
    'connected': False
}

port_new = None
port_old = None


class WindowSettings(tk.Frame):

    def __init__(self, parent, controller):
        """INIT
        ----------------------------------------------------------------------------------------------------------------
        """
        tk.Frame.__init__(self, parent)

        # create frame
        self.frame = tk.Frame(self)
        self.frame.config(height=config.windows['main_height'],
                          width=(config.windows['width'] - config.windows['sidemenu_width']),
                          bg=config.windows['mainwindow_color'],
                          padx=5, pady=5, relief=tk.RIDGE, borderwidth=1)
        self.frame.pack(side="top", fill="x", expand=True)

        gui.create_label(self.frame, label_id="PL_COM", text="COM:", x=20, y=35)
        gui.create_label(self.frame, label_id="PL_baud_rate", text="Baud rate:", x=20, y=65)

        # read user PORT
        try:
            with open(config.directory_config) as json_data:
                config_data = json.load(json_data)
        except (OSError, ValueError, KeyError) as error:
            print("Could not read {0}: {1}".format(config.directory_config, error))
            config_data = {}

        global port_old
        port_old = config_data.get('power line port', 'COM4')

        gui.create_entry(self.frame, entry_id=id_entry['COM'], text=port_old,
                         height=25, width=100, x=90, y=45)
        gui.create_entry(self.frame, entry_id=id_entry['baud rate'], text="9600", height=25, width=100, x=90, y=75,
                         readonly=True)

        gui.create_button(self.frame, text="Connect", button_id=id_button['connect'],
                          width=100, height=25, x=260, y=45,
                          bg="#660D0D", fg="#ffffff", active_background="#660D0D", active_foreground="#ffffff",
                          action=lambda: self.connect())

    def connect(self):
        """connect
        ----------------------------------------------------------------------------------------------------------------
        """
        global port_old, port_new

        if not power_line.is_connected():
            port_new = gui.get_entry(id_entry['COM']).get()
            state = power_line.connect(port=port_new)
            if state:
                gui.config_button(button_id=id_button['connect'], text="connected",
                                  bg="#0C6046", active_background="#0C6046")

                # change default PORT in case of changes
                if port_old != port_new:
                    # read user PORT
                    with open(config.directory_config, 'r') as json_data:
                        config_data = json.load(json_data)
                        json_data.close()

                    config_data['power line port'] = port_new

                    # write user PORT
                    with open(config.directory_config, 'w') as json_data:
                        json.dump(config_data, json_data, ensure_ascii=False, indent=4)
                        json_data.close()

        else:
            state = power_line.disconnect()
            if state:
                gui.config_button(button_id=id_button['connect'], text="connect",
                                  bg="#660D0D", active_background="#660D0D")
