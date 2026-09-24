import tkinter as tk
import config
import panel.panel_buttons as panel_buttons
import panel.panel_main as panel_main
import panel.panel_edit as panel_edit


class WindowPanel(tk.Frame):

    def __init__(self, parent, controller):
        """INIT
        ----------------------------------------------------------------------------------------------------------------
        """
        tk.Frame.__init__(self, parent)

        '''Create main frame
        -------------------------------------------------------------------------------------------------------------'''
        self.frame = tk.Frame(self)
        self.frame.config(height=config.windows['main_height'],
                          width=(config.windows['width'] - config.windows['sidemenu_width']),
                          bg=config.windows['mainwindow_color'],
                          padx=5, pady=5, relief=tk.RIDGE, borderwidth=1)
        self.frame.pack(side="top", fill="x", expand=True)

        '''create buttons
        -------------------------------------------------------------------------------------------------------------'''
        frame_panel_buttons = tk.Frame(self)
        frame_panel_buttons.config(height=config.panel_buttons['frame_height'],
                                   width=config.panel_buttons['frame_width'],
                                   bg=config.windows['mainwindow_color'],
                                   padx=5, pady=5, relief=tk.RIDGE, borderwidth=0)
        frame_panel_buttons.place(x=config.panel_buttons['frame_x'], y=config.panel_buttons['frame_y'])

        panel_buttons.create_buttons(frame_panel_buttons)
        panel_buttons.config_buttons()
        panel_buttons.hide_buttons(hide_all=False)

        '''create main panel
        -------------------------------------------------------------------------------------------------------------'''
        frame_main = tk.Frame(self)
        frame_main.config(height=config.panel_main['frame_height'],
                          width=config.panel_main['frame_width'],
                          bg=config.windows['mainwindow_color'],
                          padx=5, pady=5, relief=tk.RIDGE, borderwidth=0)
        frame_main.place(x=config.panel_main['frame_x'], y=config.panel_main['frame_y'])

        panel_main.create(frame_main)

        '''create edit panel
        -------------------------------------------------------------------------------------------------------------'''
        frame_edit = tk.Frame(self)
        frame_edit.config(height=config.panel_edit['frame_height'],
                          width=config.panel_edit['frame_width'],
                          bg=config.windows['mainwindow_color'],
                          padx=5, pady=5, relief=tk.RIDGE, borderwidth=0)
        frame_edit.place(x=config.panel_edit['frame_x'], y=config.panel_edit['frame_y'])

        panel_edit.create(frame_edit)
        panel_edit.hide()
