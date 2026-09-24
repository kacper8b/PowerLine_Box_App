import json
import logging
import tkinter as tk

from powerline_box import config
from powerline_box import gui
from powerline_box import theme
from powerline_box.uart import power_line

logger = logging.getLogger(__name__)


# USED interfaces:
id_button = {
    'connect': "connect",
    'save_init_delay': "save_init_delay",
}

id_entry = {
    'COM': "PowerLine_COM",
    'baud rate': "PowerLine_baud",
    'init_delay': "PowerLine_init_delay",
}


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
            with open(config.directory_config, encoding='utf-8') as json_data:
                config_data = json.load(json_data)
        except (OSError, ValueError, KeyError) as error:
            logger.error("Could not read %s: %s", config.directory_config, error)
            config_data = {}

        self.port_old = config_data.get('power line port', 'COM4')
        self.port_new = None

        gui.create_entry(self.frame, entry_id=id_entry['COM'], text=self.port_old,
                         height=25, width=100, x=90, y=45)
        gui.create_entry(self.frame, entry_id=id_entry['baud rate'], text="9600", height=25, width=100, x=90, y=75,
                         readonly=True)

        gui.create_button(self.frame, text="Connect", button_id=id_button['connect'],
                          width=100, height=25, x=260, y=45,
                          bg=theme.DARK_RED, fg=theme.WHITE, active_background=theme.DARK_RED, active_foreground=theme.WHITE,
                          action=lambda: self.connect())

        # INIT command delay
        gui.create_label(self.frame, label_id="PL_init_delay",
                         text="INIT delay:", x=20, y=125)
        gui.create_label(self.frame, label_id="PL_init_delay_info",
                         text="range: ({0}-{1} ms)".format(config.INIT_DELAY_MIN, config.INIT_DELAY_MAX),
                         x=320, y=125)
        gui.create_entry(self.frame, entry_id=id_entry['init_delay'], text=str(config.get_init_delay()),
                         height=25, width=100, x=90, y=135)
        gui.create_button(self.frame, text="Save", button_id=id_button['save_init_delay'],
                          width=100, height=25, x=260, y=135,
                          bg=theme.DARK_RED, fg=theme.WHITE, active_background=theme.DARK_RED, active_foreground=theme.WHITE,
                          action=lambda: self.save_init_delay())

    def connect(self):
        """connect
        ----------------------------------------------------------------------------------------------------------------
        """
        if not power_line.is_connected():
            self.port_new = gui.get_entry(id_entry['COM']).get()
            state = power_line.connect(port=self.port_new)
            if state:
                gui.config_button(button_id=id_button['connect'], text="connected",
                                  bg=theme.GREEN, active_background=theme.GREEN)

                # change default PORT in case of changes
                if self.port_old != self.port_new:
                    # read user PORT
                    with open(config.directory_config, 'r', encoding='utf-8') as json_data:
                        config_data = json.load(json_data)

                    config_data['power line port'] = self.port_new

                    # write user PORT
                    with open(config.directory_config, 'w', encoding='utf-8') as json_data:
                        json.dump(config_data, json_data, ensure_ascii=False, indent=4)

        else:
            state = power_line.disconnect()
            if state:
                gui.config_button(button_id=id_button['connect'], text="connect",
                                  bg=theme.DARK_RED, active_background=theme.DARK_RED)

    def save_init_delay(self):
        """save_init_delay
        ----------------------------------------------------------------------------------------------------------------
        """
        raw_value = gui.get_entry(id_entry['init_delay']).get()
        try:
            value = int(raw_value)
        except ValueError:
            logger.error("Invalid INIT delay value: %s", raw_value)
            gui.config_button(button_id=id_button['save_init_delay'], text="Invalid",
                              bg=theme.DARK_RED, active_background=theme.DARK_RED)
            return

        if not (config.INIT_DELAY_MIN <= value <= config.INIT_DELAY_MAX):
            logger.error("INIT delay %s out of allowed range %s-%s", value, config.INIT_DELAY_MIN, config.INIT_DELAY_MAX)
            gui.config_button(button_id=id_button['save_init_delay'], text="Invalid",
                              bg=theme.DARK_RED, active_background=theme.DARK_RED)
            return

        try:
            with open(config.directory_config, 'r', encoding='utf-8') as json_data:
                config_data = json.load(json_data)
        except (OSError, ValueError) as error:
            logger.error("Could not read %s: %s", config.directory_config, error)
            config_data = {}

        config_data['init delay'] = value

        with open(config.directory_config, 'w', encoding='utf-8') as json_data:
            json.dump(config_data, json_data, ensure_ascii=False, indent=4)

        logger.info("Saved INIT delay: %s", value)
        gui.config_button(button_id=id_button['save_init_delay'], text="Saved",
                          bg=theme.GREEN, active_background=theme.GREEN)
