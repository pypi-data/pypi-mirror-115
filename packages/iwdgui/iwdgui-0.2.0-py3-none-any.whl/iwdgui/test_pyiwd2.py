#!/usr/bin/env python3

"""
pyiwd_test: the pyiwd test suite
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies.

Usage: python -m unittest iwdgui.pyiwd_test

"""
import unittest
import time

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib

from . import pyiwd

PRINT = False


loop = GLib.MainLoop()
main_context = GLib.MainLoop.get_context(loop)


class test_pyiwd_station(unittest.TestCase):

    def test_lists(self):
        adap_list = pyiwd.adapter_list()
        dev_list = pyiwd.dev_list()
        dev_name = dev_list[0]["Name"]
        dev_path = pyiwd.dev_path_by_name(dev_name)
        nws_list = pyiwd.station_nws(dev_path)
        #nw_name_list = [pyiwd.nw_name_by_path(nw[0]) for nw in nws_list]
        nw_name_list = pyiwd.station_nw_name_list(dev_path)
        try:
            diags = pyiwd.station_diagnostics(dev_path)
        except:
            diags = {}
        print("adap_list:", adap_list)
        print("dev_list:", dev_list)
        print("nw_list :", nws_list)
        print("name_list:", nw_name_list)
        print("diags   :", diags)



    def test_rssi(self):
        name = pyiwd.dev_list()[0]["Name"]
        print("Name:", name )
        path = pyiwd.dev_path_by_name(name)
        print("Path:", path )
        nw_list = pyiwd.station_nws(path)
        print("nw_list:", nw_list )
        this_nw = nw_list[0][0]
        rssi = pyiwd.station_rssi(path, this_nw)
        print("rssi", rssi)
        try: 
            diags = pyiwd.station_diagnostics(path)
        except:
            diags = {}
        print("diags:", diags)
        print("adapter dic[" + name + "]", pyiwd.adapter_dic_by_devname(name))

    def test_nw_dic(self):
        nw_list = pyiwd.nw_list()
        print("nw_list: ", nw_list)
        nw_list_connected = pyiwd.nw_list_connected()
        print()
        print("nw_list_connected: ", nw_list_connected)
        dev_name = pyiwd.dev_list()[0]["Name"]
        nw_d_ic = pyiwd.nw_dic_connected_to_dev(dev_name)
        print("test_nw_dic, nw_d_ic", nw_d_ic)


if __name__ == '__main__':
    unittest.main()


