import tkinter as tk
import config
import gui


class WindowHome(tk.Frame):

    def __init__(self, parent, controller):
        """INIT
        --------------------------------------------------------------------------------------------------------------------
        """
        tk.Frame.__init__(self, parent)

        # create frame
        self.frame = tk.Frame(self)
        self.frame.config(height=config.windows['main_height'],
                          width=(config.windows['width'] - config.windows['sidemenu_width']),
                          bg=config.windows['mainwindow_color'],
                          padx=5, pady=5, relief=tk.RIDGE, borderwidth=1)
        self.frame.pack(side="top", fill="x", expand=True)

        gui.create_label(self.frame, label_id="Main", text="PowerLine Box", x=50, y=50)
        gui.create_label(self.frame, label_id="Main", text="- Configuration files are located in: "
                                                           "C:\\Users\\user\\Documents\\PowerLine Box", x=50, y=70)
        gui.create_label(self.frame, label_id="Main", text="- Files are created after the first start of the "
                                                           "application", x=50, y=90)
        gui.create_label(self.frame, label_id="Main", text="- Files are modified automatically", x=50, y=110)
        gui.create_label(self.frame, label_id="Main", text="- You can restore the files by deleting them and "
                                                           "restarting the application", x=50, y=130)
