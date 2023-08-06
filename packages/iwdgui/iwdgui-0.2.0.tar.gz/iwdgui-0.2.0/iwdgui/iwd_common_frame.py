#!/usr/bin/python3
"""
iwd_menu: common code for iwd_frame modules
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except:
    # If no Gtk then no error message, can only write to stderr
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent")
    sys.exit(exitcodes.IMPORT_FAILED)


#constants
FRAME_MARGIN = 2
FRAME_LABEL_XALIGN = 0.025
GRID_MARGIN = 2
GRID_ROW_SPACING = 2
GRID_COL_SPACING = 20
VALUE_LEN = 36
PROMPT_LEN = 12
COMBOBOX_LEN = 64
RIGHT = Gtk.PositionType.RIGHT
BOTTOM = Gtk.PositionType.BOTTOM


class GtkValueLabel(Gtk.Label):
    "Customized Gtk.Label class for width, alingment and selectable"
    def __init__(self):
        super().__init__()
        self.set_xalign(0)
        self.set_width_chars(VALUE_LEN)
        self.set_max_width_chars(VALUE_LEN)
        self.set_selectable(True)

def addln2grid(grid, ln, label, widget):
    """ adds a line to a grid. ln is the last leftside widget to add
    below to label is the text of the prompt, widget is the value.
    Returns the labelwidget of the created prompt"""
    prompt = Gtk.Label(label=label.ljust(PROMPT_LEN),
                       xalign=0,
                       selectable=True,
                       width_chars=PROMPT_LEN,
                       max_width_chars=PROMPT_LEN)
    grid.attach_next_to(prompt, ln, BOTTOM, 1, 1)
    grid.attach_next_to(widget, prompt, RIGHT, 1, 1)
    return prompt
