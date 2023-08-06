#!/usr/bin/python3
"""
iwd_connection_frame: code related to the connection frame
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import sys
from . import exitcodes

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except:
    # If no Gtk then no error message, can only write to stderr
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent")
    sys.exit(exitcodes.IMPORT_FAILED)

from . import pyiwd
from . import entry
from .msg_window import show_error_message
from .comboboxtext import ComboBoxText
from .wifi import wifi_channel, wifi_band, wifi_generation, \
    wifi_signal_strength
from .iwd_common_frame import FRAME_MARGIN, FRAME_LABEL_XALIGN, \
    GRID_MARGIN, GRID_ROW_SPACING, GRID_COL_SPACING, RIGHT, BOTTOM, \
    GtkValueLabel, addln2grid


#shorthand to avoid checking if a key is in a dic each time
dicstr = lambda dic, key: dic[key] if key in dic else ""
dicint = lambda dic, key: dic[key] if key in dic else 0


class ConnectionFrame(Gtk.Frame):
    "Everything related to the interface frame"

    def __init__(self, dev_name, advanced, on_line):
        """Requires the device name,·
        and callbacks for nw_combo and hidden buttons"""

        self._nw_combo = ComboBoxText()
        self._access_point_label = GtkValueLabel()
        self._radio_label = GtkValueLabel()
        self._signal_label = GtkValueLabel()
        self._sec_label = GtkValueLabel()
        self._connect_hidden_button = Gtk.Button(label="Connect hidden")
        self._dev_name = dev_name
        self._dev_path = pyiwd.dev_path_by_name(dev_name)
        self._advanced = advanced
        self._on_line = on_line

        # construct frame
        Gtk.Frame.__init__(self,
                           label="Active connection",
                           label_xalign=FRAME_LABEL_XALIGN,
                           margin=FRAME_MARGIN)
        grid = Gtk.Grid(row_spacing=GRID_ROW_SPACING,
                        column_spacing=GRID_COL_SPACING,
                        margin=GRID_MARGIN)
        grid.attach_next_to(self._nw_combo, None,
                            Gtk.PositionType.BOTTOM, 2, 1)
        self._nw_combo.connect("changed", self.nw_combo_changed)
        self.populate_nw_combo()
        self.update_nw_props(new_dev_name = dev_name)
        ln = self._nw_combo
        ln = addln2grid(grid, ln, "Access point", self._access_point_label)
        ln = addln2grid(grid, ln, "Radio", self._radio_label)
        ln = addln2grid(grid, ln, "Signal ", self._signal_label)
        ln = addln2grid(grid, ln, "Security", self._sec_label)
        hidden_button_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        hidden_button_box.pack_end(self._connect_hidden_button,
                                   False, True, 0)
        #self._connect_hidden_button.connect("clicked", connect_hidden_fn)
        self._connect_hidden_button.connect("clicked", self.connect_hidden)
        grid.attach_next_to(hidden_button_box, self._sec_label,
                            Gtk.PositionType.BOTTOM, 1, 1)
        self.add(grid)

    def set_advanced(self, flag):
        self._advanced = flag
        self.update_nw_props()

    def set_on_line(self, flag):
        self._on_line = flag
        self._connect_hidden_button.set_sensitive(flag)

    def get_ssid(self):
        return self._nw_combo.get_active_text()

    def _update_nw_combo(self, nw_name):
        "selects an entry in the nw_combo, adds it if needed"
        if not nw_name in self._nw_combo.entries():
            self._nw_combo.insert_text_sorted(nw_name)
        self._nw_combo.set_active_text(nw_name)

    def populate_nw_combo(self):
        current_nw_name = self.get_ssid()
        station_nw_name_list = pyiwd.station_nw_name_list(self._dev_path)
        self._nw_combo.update_entries(station_nw_name_list)

    def set_ap_label(self, text):
        self._access_point_label.set_text(text if text else "")

    def set_radio_label(self, text):
        self._radio_label.set_text(text if text else "")

    def set_signal_label(self, text):
        self._signal_label.set_text(text if text else "")

    def set_sec_label(self, text):
        self._sec_label.set_text(text if text else "")

    def _ap_str(self, nw_dic, diags):
        ssid = dicstr(nw_dic,'Name') if nw_dic else ""
        if len(ssid) > 0:
            if diags and self._advanced:
                retstr = "SSID: " + ssid
                retstr += ", BSSID: " + dicstr(diags, "ConnectedBss")
            else:
                retstr = ssid
        else:
            retstr = "-"
        return retstr

    def _radio_str(self, nw_dic, diags):

        standard = band = ""
        generation = frequency = channel = 0
        if diags:
            standard = dicstr(diags, "RxMode")
            frequency = dicint(diags, "Frequency")
            if frequency:
                band = wifi_band(frequency)
                channel = wifi_channel(frequency)
            if len(standard) > 0:
                generation = wifi_generation(standard_802=standard)
            elif len(band) > 0:
                generation = wifi_generation(freq_band=band)
            # continue below...
        elif nw_dic and nw_dic['Connected']:
            return "Connected"
        else:
            return "-"

        retstr = "WiFi-" + str(generation) if generation else ""
        if self._advanced:
            if len(band) > 0:
                retstr += ", " + band
            if len(standard) > 0:
                retstr += ", " + standard
            if channel > 0:
                retstr += ", channel " + str(channel)
        return retstr

    def _signal_str(self, nw_dic, diags):
        "Updates the signal strength field in the window"
        """
        strength_lst = [31, 67, 70, 80, 90, 100]
        description_lst = ["Amazing", "Strong",
                           "Good", "Poor", "Bad", "Unusable"]
        """

        sig_strength = None
        retstr = "-"
        if diags:
            sig_strength = dicint(diags,"RSSI")
        elif nw_dic:
            nw_path = dicstr(nw_dic, "KnownNetwork") 
            if len(nw_path) > 0:
                sig_strength = pyiwd.station_rssi(
                    self._dev_path, nw_dic["KnownNetwork"])
                if sig_strength:
                    sig_strength = round(sig_strength/100)

        if sig_strength:
            desc, pos = wifi_signal_strength(sig_strength)
            retstr = desc
            if self._advanced:
                retstr += ", " + str(-sig_strength) + " dBm"
                if diags:
                    rx = round(dicint(diags,"RxBitrate")/10)
                    tx = round(dicint(diags,"TxBitrate")/10)
                    if rx > 0:
                        retstr += ", Rx " + str(rx) + " Mbps"
                    if tx > 0:
                        retstr += ", Tx " + str(tx) + " Mbps"
        return retstr

    def _sec_str(self, nw_dic, diags):
        if diags:
            return dicstr(diags, "Security")
        elif nw_dic:
            return dicstr(nw_dic, 'Type')
        else:
            return "-"

    def update_nw_props(self, new_dev_name = None):
        if new_dev_name:
            self._dev_name = new_dev_name
        nw_dic = diags = None
        # get data
        try:
            nw_dic = pyiwd.nw_dic_connected_to_dev(self._dev_name)
            if nw_dic and nw_dic["Name"] != self.get_ssid():
                self._update_nw_combo(nw_dic["Name"])
        except Exception as e:
            pass
            #print("Cannot get network dic connected to", self._dev_path,
            #      "error:", e)
        try:
            diags = pyiwd.station_diagnostics(self._dev_path)
        except Exception as e:
            pass
            #print("Cannot get diags for path:", self._dev_path, "error:", e)
        self.set_ap_label(self._ap_str(nw_dic, diags))
        self.set_radio_label(self._radio_str(nw_dic, diags))
        self.set_signal_label(self._signal_str(nw_dic, diags))
        self.set_sec_label(self._sec_str(nw_dic, diags))

    def set_ssid(self, ssid):
        "Selects a ssid, inserts it in the combobox if needed"
        if ssid in self._nw_combo.entries():
            self._nw_combo.set_active_text(ssid)
        else:
            self._nw_combo.insert_text(0, None, ssid)
            self._nw_combo.set_active(0)


    def nw_combo_changed(self, widget):
        self.connect_network(self.get_ssid())

    def connect_network(self, nw_name):
        "Connects to the selected network, when on-line"
        print("connect_network", nw_name)
        nw_path = pyiwd.nw_path_by_name(nw_name)
        if self._on_line and nw_path:
            self.set_ap_label("Connecting")
            pyiwd.nw_connect_async(nw_path,
                                   self.connect_reply_handler,
                                   self.connect_error_handler)

    def connect_reply_handler(self):
        "Called on connect success"

    def connect_error_handler(self, error):
        "Called on connect failure"
        print("connect_error_handler", error)

    def disconnect_network(self):
        pyiwd.station_disconnect_async(self._devpath,
                                       self.disconnect_network_success,
                                       self.disconnect_network_error)

    def disconnect_network_success(self):
        #print("disconnect_network_success")
        pass

    def disconnect_network_error(self, error):
        print("disconnect_network_error:", error)

    def connect_hidden(self, widget):
        if not self._on_line:
            return
        entries = entry.show_hidden_essid_entry_window(self.get_toplevel())
        if not entries:
            return
        nw_name = entries[0]
        nw_passphrase = entries[1]
        self.set_ap_label("Connecting")
        self.set_signal_label("")
        self.set_sec_label("")
        pyiwd.agent.set_passphrase(nw_name, nw_passphrase)
        pyiwd.station_connect_hidden_nw_async(
            self._dev_path,
            nw_name,
            self.hidden_connect_reply_handler,
            self.hidden_connect_error_handler)

    def hidden_connect_reply_handler(self):
        nw_dic = pyiwd.nw_dic_connected_to_dev(self._dev_path)
        if nw_dic:
            nw_name = nw_dic["Name"]
            self.set_ssid(nw_name)
            self.set_ap_label(nw_name)

    def hidden_connect_error_handler(self, error):
        "Connect to hidden network failed, show error msg"
        print("hidden_connect_error_handler", error)
        self.update_nw_props()
        dbus_error = error.get_dbus_name()
        error_msg_dic = {
            "net.connman.iwd.Failed" : "Connection failed",
            "net.connman.iwd.NotFound" : "Hidden network not found",
            "net.connman.iwd.NotHidden" : "Network is not hidden",
            "net.connman.iwd.NotConnected" : "Not connected",
            "net.connman.iwd.InvalidFormat" : "Wrong password",
            "net.connman.iwd.NotConfigured" : "Not configured",
            "net.connman.iwd.InvalidArguments" : "Wrong password",
            "net.connman.iwd.ServiceSetOverlap" : "Multiple networks found",
            "net.connman.iwd.AlreadyProvisioned" : "Network already known"}
        try:
            error_msg = error_msg_dic[dbus_error]
        except KeyError:
            sys.stderr.write("hidden_connect_error_handler KeyError:"
                             + dbus_error)
            error_msg = error.get_dbus_message()
        except Exception as e:
            sys.stderr.write("hidden_connect_error_handler error:", e)
            error_msg = error.get_dbus_message()
        show_error_message(
            "Connect to hidden network failed",
            [error_msg, "(IWD/D-Bus error: "+error.get_dbus_message()+")"])






