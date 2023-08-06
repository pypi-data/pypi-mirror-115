#!/usr/bin/python3
"""
iwd_known_networks_frame: code related to the known networks  frame
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

from datetime import datetime

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except:
    # If no Gtk then no error message, can only write to stderr
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent")
    sys.exit(exitcodes.IMPORT_FAILED)


from . import pyiwd
from .comboboxtext import ComboBoxText
from .iwd_common_frame import FRAME_MARGIN, FRAME_LABEL_XALIGN, \
    GRID_MARGIN, GRID_ROW_SPACING, GRID_COL_SPACING, RIGHT, BOTTOM, \
    GtkValueLabel, addln2grid


def security_str(sec_str):
    "convert pwd to preshared key"
    result = {
        "psk" : "Pre-shared key",
        "open" : "Open",
        "8021x" : "Enterprise"
    }
    try:
        return result[sec_str]
    except KeyError:
        pass
    except Exception as e:
       sys.stderr.write("security_str, unexpected error:", e)
    return sec_str





def localdatetime(ISO_8601_str):
    "Convert an ISO_8601 time string to a local time string"
    dt_utc = datetime.fromisoformat(ISO_8601_str[:-1]+"+00:00")
    dt_tz = dt_utc.astimezone()
    return dt_tz.strftime("%c")


class KnownNetworksFrame(Gtk.Frame):
    " Everythng thing to do with the known networks frame"

    def __init__(self):
        self.known_network_combo = ComboBoxText()
        self.last_connected = GtkValueLabel()
        self.auto_connect = Gtk.CheckButton()
        self.known_nw_security = GtkValueLabel()
        self.hidden = GtkValueLabel()
        self.forget_network_button = Gtk.Button(label="Forget")

        Gtk.Frame.__init__(self,
                           label="Known networks",
                           label_xalign=FRAME_LABEL_XALIGN,
                           margin=FRAME_MARGIN)

        grid = Gtk.Grid(row_spacing=GRID_ROW_SPACING,
                                       column_spacing=GRID_COL_SPACING,
                                       margin=GRID_MARGIN)
        grid.attach_next_to(self.known_network_combo,
                                          None,
                                          Gtk.PositionType.BOTTOM, 2, 1)
        self.populate_known_network_combo_box()
        self.known_network_combo.connect(
            "changed", self.known_networks_combo_changed)
        ln = self.known_network_combo
        ln = addln2grid(grid, ln,
                        "Last connected", self.last_connected)
        ln = addln2grid(grid, ln,
                        "Auto connect", self.auto_connect)
        self.auto_connect.connect("toggled", self.auto_connect_toggled)
        ln = addln2grid(grid, ln,
                        "Security", self.known_nw_security)
        ln = addln2grid(grid, ln, "Hidden", self.hidden)
        button_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        button_box.pack_end(self.forget_network_button, False, True, 0)
        grid.attach_next_to(button_box, self.hidden,
                                           Gtk.PositionType.BOTTOM, 1, 1)
        self.forget_network_button.connect("clicked", self.forget_network)
        self.add(grid)

    def populate_known_network_combo_box(self):
        known_networks = pyiwd.known_nw_list()
        entries = [nw["Name"] for nw in known_networks]
        self.known_network_combo.update_entries(entries)
        self.known_networks_combo_changed(self.known_network_combo)

    def get_known_nw_name(self):
        return self.known_network_combo.get_active_text()

    def known_networks_combo_changed(self, widget):
        #known_network_name = widget.get_active_text()
        #known_network_name = self.get_known_nw_name()
        self.update_known_nw_info()

        """
        known_networks = pyiwd.known_nw_list()
        #FIXME: do we need a loop here, or can we get the dic directly?
        for known_network in known_networks:
            if known_network_name == known_network["Name"]:
                time_str = localdatetime(known_network["LastConnectedTime"])
                self.last_connected.set_text(time_str)
                self.auto_connect.set_active(known_network["AutoConnect"])
                self.known_nw_security.set_text(
                    security_str(known_network["Type"]))
                self.hidden.set_text(
                    "Yes" if known_network["Hidden"] else "No")
                return
        """

    def update_known_nw_info(self):
        "Updates the info on a known network"
        known_nw_dic = pyiwd.known_nw_dic_by_name(self.get_known_nw_name())
        time_str = localdatetime(known_nw_dic["LastConnectedTime"])
        self.last_connected.set_text(time_str)
        self.auto_connect.set_active(known_nw_dic["AutoConnect"])
        self.known_nw_security.set_text(
            security_str(known_nw_dic["Type"]))
        self.hidden.set_text(
            "Yes" if known_nw_dic["Hidden"] else "No")
        return


    def auto_connect_toggled(self, widget):
        "gets called when the autoconnect checkbox is toggled"
        autoconnect = widget.get_active()
        known_nw_name = self.known_network_combo.get_active_text()
        if known_nw_name:
            known_nw_path = pyiwd.known_nw_path_by_name(known_nw_name)
            pyiwd.known_nw_autoconnect(known_nw_path, autoconnect)

    def forget_network(self, widget):
        known_nw_name = self.known_network_combo.get_active_text()
        if known_nw_name:
            known_nw_path = pyiwd.known_nw_path_by_name(known_nw_name)
            pyiwd.known_nw_forget(known_nw_path)
            self.populate_known_network_combo_box()


