#!/usr/bin/env python

"""
entry: facilittes user entry from screen
(c) 2020-2021 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

# Assume gtk availability check done in krapplet.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

MIN_PASSWD_LEN = 8
BOTTOM = Gtk.PositionType.BOTTOM
RIGHT = Gtk.PositionType.RIGHT
PROMPT_LEN = 20
INPUT_LEN = 20

PASS_MIN_8 = "Passphrase is minimum 8 characters"
PASS_NOT_SAME = "Passphrases not identical"

class EntryDialog(Gtk.Dialog):
    """ PasswordEntryDialog: pops up a window to ask for a password """
    def __init__(self, title, parent_window, prompts):
        Gtk.Dialog.__init__(self, title, transient_for=parent_window, flags=0)
        self.set_destroy_with_parent(True)
        #self.set_modal(True)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                         Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        box = self.get_content_area()
        box.add(Gtk.Label())
        grid = Gtk.Grid(row_spacing=2, column_spacing=5)
        labels = []
        self.entries = []
        last_prompt = None
        for prompt in prompts:
            label = Gtk.Label(label=prompt[0].ljust(PROMPT_LEN), xalign=0)
            entry = Gtk.Entry(xalign = 0, visibility=prompt[1],
                              width_chars=INPUT_LEN)
            grid.attach_next_to(label, last_prompt, BOTTOM, 1, 1)
            grid.attach_next_to(entry, label, RIGHT, 1, 1)
            self.entries.append(entry)
            last_prompt = label
        entry.set_activates_default(True)
        box.add(grid)
        self.error_msg = Gtk.Label()
        box.add(self.error_msg)
        box.add(Gtk.Label())
        self.set_default_response(Gtk.ResponseType.OK)
        self.show_all()

    def show_error(self, error_msg):
        self.error_msg.set_markup("<b>" + error_msg + "</b>")

    def get_entries( self ) -> str:
        """ returns the entered passwd from screen """
        entries = []
        for entry in self.entries:
            entries.append(entry.get_text())
        return entries


def _show_entry_window(title, parent_window, prompts, validiation_fn):
    "Shows an entry window and returns the result"
    entries = None
    dialog = EntryDialog(title, parent_window, prompts)
    valid = False
    while not valid:
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            entries = dialog.get_entries()
            valid, error_msg = validiation_fn(entries)
            dialog.show_error(error_msg)
        else:
            # Cancel or destroy or whatever
            entries = None
            valid = True
    dialog.destroy()
    return entries


def _password_entry_validation(entries):
    "Returns a tuple if (valid_entry, error_msg)"
    valid = len(entries[0]) >= MIN_PASSWD_LEN
    error_msg = "" if valid else PASS_MIN_8
    return valid, error_msg

def show_password_entry_window(title, parent_window):
    "shows the password entry window, and returns the entered passwd"
    prompts = [("Passphrase", False)]
    entries = _show_entry_window(title, parent_window,
                                 prompts, _password_entry_validation)
    if entries:
        return entries[0]
    return ""

def _hidden_essid_entry_validation(entries):
    if entries[1] == entries[2]:
        valid = len(entries[1]) >= MIN_PASSWD_LEN
        error_msg = "" if valid else PASS_MIN_8
        return valid, error_msg
    else:
        return False, PASS_NOT_SAME


def show_hidden_essid_entry_window(parent_window):
    "Shows the hidden network entry window, and returns the entered ESSID"
    prompts = [("Network name", True),
               ("Passphrase", False),
               ("Confirm passphrase", False)]
    entries = _show_entry_window("Hidden network", parent_window,
                                  prompts, _hidden_essid_entry_validation)
    return entries

