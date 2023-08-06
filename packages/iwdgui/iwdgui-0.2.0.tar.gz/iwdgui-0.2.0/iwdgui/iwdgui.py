#!/usr/bin/env python3

"""
Iwdgui: A graphical frontend for iwd, Intel's iNet Wireless Daemon
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies
"""

import sys
import signal

from . import exitcodes

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, GLib, Gio
except:
    # If no Gtk then no error message, can only write to stderr
    sys.stderr.write("Please install gtk3 and python-gobject, or equivalent")
    sys.exit(exitcodes.IMPORT_FAILED)

# own application packages
from .msg_window import show_error_message, show_info_message
from . import pyiwd
from . import entry
#from .icon import icon_path
from .notify import Notify
from .iwd_menu import IwdMenu
from .iwd_interface_frame import InterfaceFrame
from .iwd_connection_frame import ConnectionFrame
from .iwd_known_nws_frame import KnownNetworksFrame

APPLICATION_ID = "com.gitlab.hfernh.iwdgui"
PERIODIC_TICK = 10                     # call every so often in seconds


def sigint_handler(sig, frame):      # frame is stack frame, and is ignored
    """ Signal handler for SIGINT, or Ctrl-C,
    to avoid standard Python stack dump """
    toplevels = Gtk.Window.list_toplevels()
    for toplevel in toplevels:
        toplevel.destroy()

def connection_str(b):
    "make a connection string from a bool"
    return "Connected" if b else "Not connected"

def start_scanning(dev_path):
    try:
        pyiwd.station_scan(dev_path)
    except Exception as e:
        print("start_scanning error:", e)
        pass


class IwdGuiWin(Gtk.Window):
    """ this is the main window of iwdgui """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(150, 100)
        self.set_transient_for(None)
        self.set_keep_above(True)
        self.connect("destroy", self.close_window)
        self.notify = Notify()
        self.tab= {}
        self.if_frame = {}
        self.conn_frame = {}
        pyiwd.agent.set_passwd_entry_callback(self.passwd_entry_callback)
        pyiwd.agent.set_release_callback(self.agent_released)

        # construct window
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.menu = IwdMenu(self.advanced_callback, self.close_window)
        box.add(self.menu)
        box.add(Gtk.Label())
        self.notebook = Gtk.Notebook()
        self.dev_name_list = pyiwd.dev_name_in_mode_list('station')
        if len(self.dev_name_list) == 0:
            show_error_message("No devices in station mode", "",
                               exitcode=exitcodes.NO_DEVICES_IN_STATION_MODE)
            return
        self.dev_name_list.sort()
        for dev_name in self.dev_name_list:
            tab = self.construct_tab(dev_name)
            if tab:
                self.tab[dev_name] = tab
                self.notebook.append_page(self.tab[dev_name],
                                          Gtk.Label(dev_name))
        box.add(self.notebook)
        box.add(Gtk.Label())
        self.known_nws_frame = KnownNetworksFrame()
        box.add(self.known_nws_frame)
        self.add(box)

        pyiwd.register_props_changed_callback(
            self.handle_dbus_signal_properties_changed)
        GLib.timeout_add_seconds(PERIODIC_TICK, self.periodic_props_update)
        self.show_all()

    def construct_tab(self, dev_name):
        "returns a box that can be placed in a tab"
        dev = pyiwd.dev_dic_by_name(dev_name)
        if dev['Mode'] != "station":
            show_info_message("Interface "
                              + dev_name
                              + " in not yet supported mode "
                              + dev['Mode'],
                              "Iwdgui currently only supports station mode")
            return None
        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        box.add(Gtk.Label())
        self.if_frame[dev_name] = InterfaceFrame(dev_name,
                                                 self.on_line_toggled)
        box.add(self.if_frame[dev_name])
        box.add(Gtk.Label())
        self.conn_frame[dev_name] = ConnectionFrame(
            dev_name, self.get_advanced(), self.on_line(dev_name))
        box.add(self.conn_frame[dev_name])
        return box

    def dev_path(self, dev_name):
        #return pyiwd.dev_path_by_name(self.dev_name())
        return self.if_frame[dev_name].get_dev_path()

    def nw_name(self, dev_name):
        #return self.conn_frame.get_ssid()
        return self.conn_frame[dev_name].get_ssid()

    def nw_path(self, dev_name):
        return pyiwd.nw_path_by_name(self.nw_name(dev_name))

    def on_line(self, dev_name):
        "returns is the on_line checkbutton is checked"
        return self.if_frame[dev_name].get_on_line_status()

    def connected(self, dev_name):
        "Checks if we are connected to a network"
        nw_dic = pyiwd.nw_dic_connected_to_dev(self.dev_path(dev_name))
        return nw_dic != None

    def advanced_callback(self):
        "Switches between basic and advanced view modes"
        #widget is a menuiten, it's child is a checkbutton
        adv = self.get_advanced()
        for dev_name in self.dev_name_list:
            self.conn_frame[dev_name].set_advanced(adv)

    def get_advanced(self):
        return self.menu.get_advanced_view()

    def add_tab(self, dev_name):
        tab = self.construct_tab(dev_name)
        if tab:
            self.tab[dev_name] = tab
            self.notebook.append_page(self.tab[dev_name], Gtk.Label(dev_name))
            self.notebook.show_all()
            self.dev_name_list.append(dev_name)

    def remove_tab(self, dev_name):
        for widget_dic in [self.if_frame, self.conn_frame, self.tab]:
            widget_dic[dev_name].destroy()
            widget_dic.pop(dev_name)
        self.dev_name_list.remove(dev_name)

    def tab_admin_check(self, dev_name):
        """Creates tab for unknown devices
        - deletes them for devices
        - that do not exist anymorei
        - returns None if the dev_name is no longer valid,
          otherwise dev_name"""

        if dev_name in self.dev_name_list:              # in our admin
            if not dev_name in pyiwd.dev_name_list():   # bur for real
                self.remove_tab(dev_name)
                return None
        else:
            self.add_tab(dev_name)
        return dev_name


    def dev_check(self, iface, path):
        dev_name = None
        table = {
            "Device" : path,
            "Station" : path,
            "Network" : pyiwd.nw_devpath_by_nwpath(path),
            "KnownNetwork" : None }
        dev_path = table[iface]
        if dev_path:
            try:
                dev_name = pyiwd.dev_name_by_path(dev_path)
            except Exception as e:
                pass
        if dev_name:
            dev_name = self.tab_admin_check(dev_name)
        return dev_name, dev_path 


    def handle_dbus_signal_properties_changed(self, interface,
                                             changed, invalidated, path):
        #dev_path = self.dev_path()
        iface = interface[interface.rfind(".") + 1:]
        for name, value in changed.items():
            if iface != "Station" and name != "Scanning":
                print("{%s} [%s] %s = %s" % (iface, path, name, value))
            dev_name, dev_path = self.dev_check(iface, path)
            if dev_name and iface == "Station":
                if name == "State":
                    self.conn_frame[dev_name].set_ap_label(value)
                    if value == "disconnected":
                        self.notify.msg(dev_name + " disconnected")
                    elif value == "connected":
                        self.conn_frame[dev_name].update_nw_props()
                elif name == "Connected":
                    self.conn_frame[dev_name].set_ap_label(
                        connection_str(value))
                elif name == "ConnectedNetwork":
                    network = pyiwd.nw_dic_by_path(value)
                    #self.conn_frame[dev_name].set_ssid(network["Name"])
                    self.conn_frame[dev_name].update_nw_props()
                    self.notify.msg(dev_name 
                                    + " Connected to " 
                                    + network["Name"])
                elif name == "Scanning":
                    if not value:
                        self.conn_frame[dev_name].populate_nw_combo()
                else:
                    print("ERROR, station change not caught")
            elif dev_name and iface == "Network":
                if name == "Connected":
                    self.conn_frame[dev_name].set_ap_label(
                        connection_str(value))
                elif name == "KnownNetwork":
                    known_nw_list = pyiwd.known_nw_list()
                    entries = [nw["Name"] for nw in known_nw_list]
                    self.known_nws_frame.populate_known_network_combo_box()
                else:
                    print("network change not caught")
            elif (dev_name
                  and dev_name in self.dev_name_list
                  and iface == "Device"
                  and name == "Powered"
                  and not value):
                self.remove_tab(dev_name)
            elif iface == "KnownNetwork":
                self.known_nws_frame.populate_known_network_combo_box()
                self.known_nws_frame.update_known_nw_info()
            else:
                print("other update not caught")

    def passwd_entry_callback(self, path):
        nw_dic = pyiwd.nw_dic_by_path(path)
        return entry.show_password_entry_window(nw_dic["Name"], self)

    def agent_released(self):
        print("Iwd stopped, agent released: terminating")
        self.destroy()

    def on_line_toggled(self, widget, dev_name):
        "called when the on_line checkbox is toggled"
        on_line = widget.get_active()
        self.conn_frame[dev_name].set_on_line(on_line)
        if widget.get_active():
            nw_path = self.nw_path(dev_name)
            nw_name = self.nw_name(dev_name)

            if nw_path:
                self.conn_frame[dev_name].connect_network(nw_name)
        else:
            self.if_frame[dev_name].disconnect_network()

    def periodic_props_update(self):

        for dev_name in self.dev_name_list:
            if self.tab_admin_check(dev_name):
                dev_path = self.dev_path(dev_name)
                start_scanning(dev_path)
                self.if_frame[dev_name].update_ip_addresses()
                self.conn_frame[dev_name].update_nw_props()
        return True

    def close_window(self, widget):
        self.destroy()


class IwdGuiApp(Gtk.Application):
    "Main application class"

    def __init__(self,*args, **kwargs):
        super().__init__(
            *args,
            application_id=APPLICATION_ID,
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        if not self.window:
            self.window = IwdGuiWin(application=self,
                                    title="Iwdgui", modal=True)
        self.window.present()

    def do_command_line(self, command_line):
        self.activate()
        return 0

    def remove_window(self):
        self.remove_window(self.window)

def main():
    " iwdgui main "
    # ignore GTK deprecation warnings gwhen not in development mode
    # for development mode, run program as python3 -X dev iwdgui
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")

    signal.signal(signal.SIGINT, sigint_handler)
    app = IwdGuiApp()
    app.run(sys.argv)

if __name__ == "__main__":
    main()

