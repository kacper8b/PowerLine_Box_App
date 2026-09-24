import tkinter as tk

from powerline_box import config
from powerline_box import gui
from powerline_box import theme

# USED interfaces:
id_button = {
    'home': "sidebar_home",
    'panel': "sidebar_panel",
    'setting': "sidebar_setting",
    'about': "sidebar_about"
}


class WindowSidebar(tk.Frame):

    def __init__(self, parent, controller):
        """INIT
        ----------------------------------------------------------------------------------------------------------------
        """
        tk.Frame.__init__(self, parent)

        # create frame
        self.frame = tk.Frame(self)
        self.frame.config(height=800, width=config.windows['sidemenu_width'],
                          bg=config.windows['sidemenu_color'], padx=5, pady=5, relief=tk.RIDGE, borderwidth=1)
        self.frame.pack(side="top", fill="both", expand=True)

        # create buttons
        gui.create_button(self.frame, button_id=id_button['home'], height=35, width=100, text="Home",
                          relx=0.5, y=30, action=lambda: controller.show_frame("WindowHome"),
                          bg=theme.BLUE, fg=theme.WHITE,
                          active_background=theme.BLUE, active_foreground=theme.WHITE)
        gui.create_button(self.frame, button_id=id_button['panel'], height=35, width=100, text="Control Panel",
                          relx=0.5, y=70, action=lambda: controller.show_frame("WindowPanel"),
                          bg=theme.BLUE, fg=theme.WHITE,
                          active_background=theme.BLUE, active_foreground=theme.WHITE)
        gui.create_button(self.frame, button_id=id_button['setting'], height=35, width=100, text="Settings",
                          relx=0.5, y=110, action=lambda: controller.show_frame("WindowSettings"),
                          bg=theme.BLUE, fg=theme.WHITE,
                          active_background=theme.BLUE, active_foreground=theme.WHITE)
        gui.create_button(self.frame, button_id=id_button['about'], height=35, width=100, text="About",
                          relx=0.5, y=150, action=lambda: controller.show_frame("WindowAbout"),
                          bg=theme.BLUE, fg=theme.WHITE,
                          active_background=theme.BLUE, active_foreground=theme.WHITE)
