"""
icon: functions and consts re icons for iwd
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

ICONNAME = "iwdgui"

def icon_path(iconname=ICONNAME, res=48):
    """ finds the path to an icon, based on std Gtk functions,
    so looking in standard locations like $HOME/.icons,
    $XDG_DATA_DIRS/icons, and /usr/share/pixmaps """
    icon_theme = Gtk.IconTheme.get_default()
    icon = icon_theme.lookup_icon(iconname, res, 0)
    if icon:
        path = icon.get_filename()
        return path
    return ""


