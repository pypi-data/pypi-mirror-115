#!/usr/bin/python3
"""
iwd_interface_frame: code related to the interface frame
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import socket

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except:
    # If no Gtk then no error message, can only write to stderr
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent")
    sys.exit(exitcodes.IMPORT_FAILED)

from . import exitcodes
from .msg_window import show_error_message

try:
    from  netifaces import ifaddresses, AF_LINK, AF_INET, AF_INET6
except Exception as e:
    show_error_message("Please install netifaces", str(e),
                       exitcode=exitcodes.IMPORT_FAILED)


from . import pyiwd

"""
from .comboboxtext import ComboBoxText
"""

from .iwd_common_frame import FRAME_MARGIN, FRAME_LABEL_XALIGN, \
    GRID_MARGIN, GRID_ROW_SPACING, GRID_COL_SPACING, VALUE_LEN, RIGHT,\
    BOTTOM, GtkValueLabel, addln2grid



def get_netifaces_addr(iface, addr_type):

    try:
        addresses = ifaddresses(iface)[addr_type]
        return addresses
    except Exception as e:
        return None


class InterfaceFrame(Gtk.Frame):
    "Everything related to the interface frame"

    def __init__(self, dev_name, on_line_toggled):
        # create widget we need to refer to
        #self._interface_combo = ComboBoxText()
        self._on_line_checkbutton = Gtk.CheckButton()
        self._vendor = GtkValueLabel()
        self._model = GtkValueLabel()
        self._ipv4_address = GtkValueLabel()
        self._ipv6_supoort = socket.has_ipv6
        self._dev_name = dev_name
        self._dev_path = pyiwd.dev_path_by_name(dev_name)
        if self._ipv6_supoort:
            self._ipv6_address = GtkValueLabel()
        adapter_dic = None

        # construct frame
        Gtk.Frame.__init__(self, label="Wireless interface",
                           label_xalign=FRAME_LABEL_XALIGN,
                           margin=FRAME_MARGIN)
        device_grid = Gtk.Grid(row_spacing=GRID_ROW_SPACING,
                               column_spacing=GRID_COL_SPACING,
                               margin=GRID_MARGIN)

        ln = addln2grid(
            device_grid, None, "On-line",self._on_line_checkbutton)
        self._adapter_dic = self._get_adapter_dic()
        ln = addln2grid(device_grid, ln, "Vendor", self._vendor)
        self.set_vendor_name(self._adapter_dic['Vendor'])
        ln = addln2grid(device_grid, ln, "Model", self._model)
        self.set_model_name(self._adapter_dic["Model"])
        self._on_line_checkbutton.set_active(True) #FIXME set to actual status
        self._on_line_checkbutton.connect(
            "toggled", on_line_toggled, dev_name)
        ln = addln2grid(device_grid, ln, "IPv4 address", self._ipv4_address)
        if self._ipv6_supoort:
            ln = addln2grid(device_grid, ln,
                            "IPv6 address", self._ipv6_address)
        self.update_ip_addresses()
        self.add(device_grid)

    def get_dev_path(self):
        return self._dev_path

    def _get_adapter_dic(self):
        adapter_dic = pyiwd.adapter_dic_by_devname(self._dev_name)
        return adapter_dic

    def set_vendor_name(self, vendor):
        self._vendor.set_text(vendor[:VALUE_LEN])

    def set_model_name(self, model):
        self._model.set_text(model[:VALUE_LEN])

    def set_ipv4_address(self, ipv4_address):
        self._ipv4_address.set_text(ipv4_address)
        return ipv4_address

    def set_ipv6_address(self, ipv6_address):
        if self._ipv6_supoort:
            self._ipv6_address.set_text(ipv6_address)
        return ipv6_address

    def set_on_line_status(self, on_off):
        self._on_line_checkbutton.set_active(on_off)
        return on_off

    def get_on_line_status(self):
        return self._on_line_checkbutton.get_active()

    def update_ipvX_address(self, family, update_fn):
        "Updates an IPv4/6 addr, requires a family and an update function"
        ip_addr_lst = get_netifaces_addr(self._dev_name, family)
        update_fn(ip_addr_lst[0]['addr'] if ip_addr_lst else "")

    def update_ipv4_address(self):
        self.update_ipvX_address(AF_INET, self.set_ipv4_address)

    def update_ipv6_address(self):
        if self._ipv6_supoort:
            self.update_ipvX_address(AF_INET6, self.set_ipv6_address)

    def update_ip_addresses(self):
        self.update_ipv4_address()
        if self._ipv6_supoort:
            self.update_ipv6_address()

    def disconnect_network(self):
        pyiwd.station_disconnect_async(self._dev_path,
                                       self.disconnect_network_success,
                                       self.disconnect_network_error)

    def disconnect_network_success(self):
        #print("disconnect_network_success")
        pass

    def disconnect_network_error(self, error):
        print("disconnect_network_error:", error)

