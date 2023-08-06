#!/usr/bin/env python

"""
msg_window: functions for showing info or erorr message
(c) 2020-2021 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import sys

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

from . import exitcodes

def show_info_or_error_message(primary_msg, secondary_msg,
                               msg_type, title, buttons ):
    """Shows an error or info  message dialog"""
    dialog = Gtk.MessageDialog(title=title, 
                               flags=0, message_type=msg_type,
                               buttons=buttons, text=primary_msg)
    if secondary_msg:
        if isinstance(secondary_msg, list):
            secmsg = '\n'.join([ln for ln in secondary_msg])
        elif isinstance(secondary_msg, str):
            secmsg = secondary_msg
        else:
            show_error_message("Internal error: show_info_or_error_message",
                               "secondary message is list nor str",
                               exitcode=exitcodes.INTERNAL_ERROR)
            """
            print("show_info_or_error_message:"
                  + " secondary message is list nor str",
                  file=sys.stderr)   """
        dialog.format_secondary_text(secmsg)
    dialog.run()
    dialog.destroy()


def show_error_message(primary_msg, secondary_msg, exitcode=0):
    """Shows an error message dialog"""
    if exitcode:
        secondary_msg = "Error " + str(exitcode) + ": " + secondary_msg
    show_info_or_error_message(primary_msg, secondary_msg,
                               Gtk.MessageType.ERROR, "IWDGUI ERROR",
                               Gtk.ButtonsType.CLOSE)
    if exitcode:
        sys.exit(exitcode)


def show_info_message(primary_msg, secondary_msg, exitcode=0):
    """ Shows an informational message dialog """
    show_info_or_error_message(primary_msg, secondary_msg,
                               Gtk.MessageType.INFO, "Informational",
                               Gtk.ButtonsType.CLOSE)

