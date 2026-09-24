import tkinter as tk
import config
import gui

# USED interfaces:
id_text = {
    'log': "change_log",
}

class WindowAbout(tk.Frame):

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

        gui.create_label(self.frame, text="Authors:", x=50, y=50)
        gui.create_label(self.frame, text="- Software: Kacper Bajda", x=50, y=70)
        gui.create_label(self.frame, text="- Hardware: Krzysztof Ciereniewicz & Michał Rzeszut", x=50, y=90)

        gui.create_label(self.frame, text="Version:", x=50, y=130)
        gui.create_label(self.frame, text="- v1.1", x=50, y=150)
        gui.create_label(self.frame, text="- date: 01.08.2022", x=50, y=170)

        gui.create_label(self.frame, text="Contact persons:", x=50, y=210)
        gui.create_label(self.frame, text="- bugfix, new features, documentation: Kacper Bajda "
                                          "[kacper.bajda@somfy.com]", x=50, y=230)
        gui.create_label(self.frame, text="- hardware issue: Krzysztof Ciereniewicz "
                                          "[krzysztof.ciereniewicz@somfy.com]", x=50, y=250)

        # create change log
        gui.create_text(text_id=id_text['log'], frame=self.frame,
                        height=config.change_log['height'], width=config.change_log['width'],
                        x=config.change_log['x'], y=config.change_log['y'],
                        readonly=True, background="#D8DDE3")

        # should be improved (separate file)

        gui.add_text(text_id=id_text['log'], new_text="Change Log:")
        gui.add_text(text_id=id_text['log'], new_text="\nVersion v1.0 (17.03.2022)")
        gui.add_text(text_id=id_text['log'], new_text="- Initial version")

        gui.add_text(text_id=id_text['log'], new_text="\nVersion v1.1 (01.08.2022)")
        gui.add_text(text_id=id_text['log'], new_text="- Panel Main Buttons: Keep only On/Off for Power Supply (remove Safe_on, Safe_off)")
        gui.add_text(text_id=id_text['log'], new_text="- Panel: Add DPC button (double power cut)")
        gui.add_text(text_id=id_text['log'], new_text="- Panel Main Buttons: Init always cause enter in power line protocol (sent power off at the begin)")
        gui.add_text(text_id=id_text['log'], new_text="- Panel: Fix minor bugs")
        gui.add_text(text_id=id_text['log'], new_text="- Console: text displayed at the end of line")
