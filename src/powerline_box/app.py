
import os
import sys
import tkinter as tk

from powerline_box import config
from powerline_box.windows.about import WindowAbout
from powerline_box.windows.home import WindowHome
from powerline_box.windows.panel_view import WindowPanel
from powerline_box.windows.settings import WindowSettings
from powerline_box.windows.sidebar import WindowSidebar
from powerline_box.windows.terminal_view import WindowTerminal


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


def _on_closing(app):
    """on_closing frame
      ------------------------------------------------------------------------------------------------------------------
      """
    app.destroy()
    os.system('taskkill /f /im powerline-box.exe')
    sys.exit


def run():
    """run
    Builds and starts the PowerLine Box application window.
    ----------------------------------------------------------------------------------------------------------------
    """
    config.configuration_init()
    app = WindowManager()
    app.title("PowerLine Box")
    app.iconbitmap(config.ICON_PATH)
    app.protocol("WM_DELETE_WINDOW", lambda: _on_closing(app))
    app.mainloop()
