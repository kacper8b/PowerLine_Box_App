
import tkinter as tk

import config
from windows.sidebar import *
from windows.panel import *
from windows.terminal import *
from windows.home import *
from windows.settings import *
from windows.about import *
import gui_terminal.terminal_main as terminal

import sys
import os


class WindowManager(tk.Tk):

    def __init__(self, *args, **kwargs):
        """INIT
        ----------------------------------------------------------------------------------------------------------------
        """

        tk.Tk.__init__(self, *args, **kwargs)

        # geometry
        self.geometry("{0}x{1}".format(config.windows['width'], config.windows['height']))
        self.resizable(width=False, height=False)

        # Frames
        frame_sidemenu = tk.Frame(self, bg="red",
                                  width=config.windows['sidemenu_width'],
                                  height=config.windows['height'])
        frame_sidemenu.grid(column=0, row=0, rowspan=2)

        frame_main = tk.Frame(self, bg="blue",
                              width=(config.windows['width'] - config.windows['sidemenu_width']),
                              height=config.windows['main_height'])
        frame_main.grid(column=1, row=0)

        frame_terminal = tk.Frame(self, bg="black",
                                  width=(config.windows['width'] - config.windows['sidemenu_width']),
                                  height=config.windows['terminal_height'])
        frame_terminal.grid(column=1, row=1)

        # Create sidebar
        window_sidebar = WindowSidebar(parent=frame_sidemenu, controller=self)
        window_sidebar.grid(row=0, column=0, sticky="nsew")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.frames = {}

        for F in (WindowHome, WindowSettings, WindowPanel, WindowAbout):
            page_name = F.__name__
            frame = F(parent=frame_main, controller=self)
            frame.grid_propagate(False)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        # initial window
        self.show_frame("WindowHome")

        # Create terminal
        window_terminal = WindowTerminal(parent=frame_terminal, controller=self)
        window_terminal.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """show frame
        ----------------------------------------------------------------------------------------------------------------
        """
        frame = self.frames[page_name]
        frame.tkraise()


def on_closing():
    """on_closing frame
      ------------------------------------------------------------------------------------------------------------------
      """
    app.destroy()
    os.system('taskkill /f /im powerline-box.exe')
    sys.exit


config.configuration_init()
app = WindowManager()
app.title("PowerLine Box")
app.iconbitmap("powerline-box.ico")
app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()

