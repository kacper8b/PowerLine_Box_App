import tkinter as tk

from powerline_box import config
from powerline_box import gui
from powerline_box import theme
from powerline_box.automation import editor
from powerline_box.panel import buttons as panel_buttons


class WindowAutomation(tk.Frame):

    def __init__(self, parent, controller):
        """INIT
        ----------------------------------------------------------------------------------------------------------------
        """
        tk.Frame.__init__(self, parent)

        self.frame = tk.Frame(self)
        self.frame.config(height=config.windows['main_height'],
                          width=(config.windows['width'] - config.windows['sidemenu_width']),
                          bg=config.windows['mainwindow_color'],
                          padx=5, pady=5, relief=tk.RIDGE, borderwidth=1)
        self.frame.pack(side="top", fill="x", expand=True)

        layout = config.automation

        '''Saved scripts (left column)
        -------------------------------------------------------------------------------------------------------------'''
        gui.create_label(self.frame, label_id="Automation", text="Saved scripts:",
                         x=layout['scripts_label_x'], y=layout['scripts_label_y'])
        gui.create_listbox(self.frame, listbox_id=editor.id_listbox['scripts'],
                           x=layout['scripts_listbox_x'], y=layout['scripts_listbox_y'],
                           width=layout['scripts_listbox_width'], height=layout['scripts_listbox_height'])

        gui.create_label(self.frame, label_id="Automation", text="Name:",
                         x=layout['name_label_x'], y=layout['name_label_y'])
        gui.create_entry(self.frame, entry_id=editor.id_entry['script_name'], text="",
                         x=layout['name_entry_x'], y=layout['name_entry_y'],
                         width=layout['name_entry_width'], height=layout['name_entry_height'])

        bx = layout['script_buttons_x']
        by = layout['script_buttons_y']
        bw = layout['script_buttons_width']
        bh = layout['script_buttons_height']
        bd = layout['script_buttons_distance_x']
        gui.create_button(self.frame, text="New", width=bw, height=bh, x=bx + 0 * (bw + bd), y=by,
                          action=lambda: editor.new_script())
        gui.create_button(self.frame, text="Load", width=bw, height=bh, x=bx + 1 * (bw + bd), y=by,
                          action=lambda: editor.load_selected())
        gui.create_button(self.frame, text="Save As", width=bw + 10, height=bh, x=bx + 2 * (bw + bd), y=by,
                          action=lambda: editor.save_as())
        gui.create_button(self.frame, text="Delete", width=bw, height=bh, x=bx + 3 * (bw + bd) + 10, y=by,
                          action=lambda: editor.delete_selected())

        '''Step list (right column)
        -------------------------------------------------------------------------------------------------------------'''
        gui.create_label(self.frame, label_id="Automation", text="Steps:",
                         x=layout['steps_label_x'], y=layout['steps_label_y'])
        gui.create_listbox(self.frame, listbox_id=editor.id_listbox['steps'],
                           x=layout['steps_listbox_x'], y=layout['steps_listbox_y'],
                           width=layout['steps_listbox_width'], height=layout['steps_listbox_height'],
                           multiple=True)

        sx = layout['side_buttons_x']
        ssx = layout['side_small_buttons_x']
        sw = layout['side_buttons_width']
        sh = layout['side_buttons_height']
        gui.create_button(self.frame, text="Remove", width=sw, height=sh, x=sx, y=layout['remove_button_y'],
                          action=lambda: editor.remove_selected())
        gui.create_button(self.frame, text="Move Up", width=sw, height=sh, x=sx, y=layout['move_up_button_y'],
                          action=lambda: editor.move_selected(-1))
        gui.create_button(self.frame, text="Move Down", width=sw, height=sh, x=sx, y=layout['move_down_button_y'],
                          action=lambda: editor.move_selected(1))

        gui.create_label(self.frame, label_id="Automation", text="Loop repeat:",
                         x=sx, y=layout['loop_repeat_label_y'])
        gui.create_entry(self.frame, entry_id=editor.id_entry['loop_repeat'], text="1",
                         x=sx, y=layout['loop_repeat_entry_y'],
                         width=layout['loop_repeat_entry_width'], height=sh)
        gui.create_button(self.frame, text="Group -> Loop", width=sw, height=sh, x=sx, y=layout['group_loop_button_y'],
                          action=lambda: editor.group_into_loop())
        gui.create_button(self.frame, text="Ungroup Loop", width=sw, height=sh, x=sx, y=layout['ungroup_loop_button_y'],
                          action=lambda: editor.ungroup_loop())

        '''Direct hardware control: behaves exactly like the Control Panel's own
        buttons (same functions, same state machine) - colored to stand out from the
        gray script-building controls, so the user can jog the motor at any time.
        -------------------------------------------------------------------------------------------------------------'''
        qcw = layout['quick_col_width']
        qcd = layout['quick_col_distance_x']
        gui.create_button(self.frame, button_id=editor.id_button['quick_init'], text="INIT", width=sw, height=sh,
                          x=sx, y=layout['quick_init_button_y'],
                          bg=theme.GREEN, fg=theme.WHITE, active_background=theme.GREEN, active_foreground=theme.WHITE,
                          action=lambda: editor.control_init(editor.id_button['quick_init']))
        gui.create_button(self.frame, button_id=editor.id_button['quick_on'], text="ON", width=qcw, height=sh,
                          x=ssx, y=layout['quick_on_off_button_y'],
                          bg=theme.GREEN, fg=theme.WHITE, active_background=theme.GREEN, active_foreground=theme.WHITE,
                          action=lambda: editor.control_on())
        gui.create_button(self.frame, button_id=editor.id_button['quick_off'], text="OFF", width=qcw, height=sh,
                          x=ssx + qcw + qcd, y=layout['quick_on_off_button_y'],
                          bg=theme.GREEN, fg=theme.WHITE, active_background=theme.GREEN, active_foreground=theme.WHITE,
                          action=lambda: editor.control_off())
        gui.create_button(self.frame, button_id=editor.id_button['quick_up'], text="Up", width=qcw, height=sh,
                          x=ssx, y=layout['quick_up_down_button_y'],
                          bg=theme.DARK_RED, fg=theme.WHITE, active_background=theme.DARK_RED,
                          active_foreground=theme.WHITE,
                          action=lambda: editor.control_panel_button(editor.id_button['quick_up'], "Up"))
        gui.create_button(self.frame, button_id=editor.id_button['quick_down'], text="Down", width=qcw, height=sh,
                          x=ssx + qcw + qcd, y=layout['quick_up_down_button_y'],
                          bg=theme.DARK_RED, fg=theme.WHITE, active_background=theme.DARK_RED,
                          active_foreground=theme.WHITE,
                          action=lambda: editor.control_panel_button(editor.id_button['quick_down'], "Down"))
        gui.create_button(self.frame, button_id=editor.id_button['quick_stop'], text="Stop", width=sw, height=sh,
                          x=sx, y=layout['quick_stop_button_y'],
                          bg=theme.DARK_RED, fg=theme.WHITE, active_background=theme.DARK_RED,
                          active_foreground=theme.WHITE,
                          action=lambda: editor.control_panel_button(editor.id_button['quick_stop'], "Stop"))

        '''Add step controls
        -------------------------------------------------------------------------------------------------------------'''
        gui.create_label(self.frame, label_id="Automation", text="Add command:",
                         x=layout['command_label_x'], y=layout['command_label_y'])
        gui.create_dropdown(self.frame, dropdown_id=editor.id_dropdown['command'],
                            values=[button['name'] for button in panel_buttons.list_buttons()],
                            x=layout['command_dropdown_x'], y=layout['command_dropdown_y'],
                            width=layout['command_dropdown_width'], height=layout['command_dropdown_height'])
        gui.create_button(self.frame, text="Add Command",
                          width=layout['add_command_button_width'], height=layout['add_command_button_height'],
                          x=layout['add_command_button_x'], y=layout['add_command_button_y'],
                          action=lambda: editor.add_command_step())

        gui.create_label(self.frame, label_id="Automation", text="Wait (ms):",
                         x=layout['wait_label_x'], y=layout['wait_label_y'])
        gui.create_entry(self.frame, entry_id=editor.id_entry['wait_ms'], text="500",
                         x=layout['wait_entry_x'], y=layout['wait_entry_y'],
                         width=layout['wait_entry_width'], height=layout['wait_entry_height'])
        gui.create_button(self.frame, text="Add Wait",
                          width=layout['add_wait_button_width'], height=layout['add_wait_button_height'],
                          x=layout['add_wait_button_x'], y=layout['add_wait_button_y'],
                          action=lambda: editor.add_wait_step())

        gui.create_dropdown(self.frame, dropdown_id=editor.id_dropdown['sequence'],
                            values=editor.preset_names(),
                            x=layout['sequence_dropdown_x'], y=layout['sequence_dropdown_y'],
                            width=layout['sequence_dropdown_width'], height=layout['sequence_dropdown_height'])
        gui.create_button(self.frame, text="Add Sequence/Script",
                          width=layout['add_sequence_button_width'], height=layout['add_sequence_button_height'],
                          x=layout['add_sequence_button_x'], y=layout['add_sequence_button_y'],
                          action=lambda: editor.add_sequence_step())

        '''Run controls
        -------------------------------------------------------------------------------------------------------------'''
        gui.create_label(self.frame, label_id="Automation", text="Repeat script:",
                         x=layout['script_repeat_label_x'], y=layout['script_repeat_label_y'])
        gui.create_entry(self.frame, entry_id=editor.id_entry['script_repeat'], text="0",
                         x=layout['script_repeat_entry_x'], y=layout['script_repeat_entry_y'],
                         width=layout['script_repeat_entry_width'], height=layout['script_repeat_entry_height'])
        gui.create_button(self.frame, text="Run",
                          width=layout['run_button_width'], height=layout['run_button_height'],
                          x=layout['run_button_x'], y=layout['run_button_y'],
                          bg=theme.GREEN, fg=theme.WHITE, active_background=theme.GREEN, active_foreground=theme.WHITE,
                          action=lambda: editor.run())
        gui.create_button(self.frame, text="Stop",
                          width=layout['stop_button_width'], height=layout['stop_button_height'],
                          x=layout['stop_button_x'], y=layout['stop_button_y'],
                          bg=theme.DARK_RED, fg=theme.WHITE, active_background=theme.DARK_RED,
                          active_foreground=theme.WHITE,
                          action=lambda: editor.stop())

        editor.refresh()
