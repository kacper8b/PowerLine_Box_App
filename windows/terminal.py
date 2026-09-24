import tkinter as tk
import config
import gui
import gui_terminal.terminal_main as terminal

# USED interfaces:
id_button = {
    'clear': "terminal_clear",
}


class WindowTerminal(tk.Frame):

    def __init__(self, parent, controller):
        """INIT
        ----------------------------------------------------------------------------------------------------------------
        """
        tk.Frame.__init__(self, parent)

        # create frame
        self.frame = tk.Frame(self)
        self.frame.config(height=config.windows['terminal_height'],
                          width=(config.windows['width'] - config.windows['sidemenu_width']),
                          bg=config.windows['sidemenu_color'], padx=5, pady=5, relief=tk.RIDGE, borderwidth=1)
        self.frame.pack(side="top", fill="x", expand=True)

        terminal.create_terminal(frame=self.frame, height=config.terminal['height'], width=config.terminal['width'],
                                 x=config.terminal['x'], y=config.terminal['y'], readonly=True)

        gui.create_button(frame=self.frame, text="clear", button_id=id_button['clear'],
                          width=config.terminal['button_width'], height=config.terminal['button_height'],
                          x=config.terminal['button_x'], y=config.terminal['button_y'],
                          bg="#000000", fg="#ffffff", active_background="#000000", active_foreground="#ffffff",
                          action=lambda: terminal.clear())
