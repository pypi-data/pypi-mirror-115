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


class test_device_in_station_mode(unittest.TestCase):

    def test_devs_in_station_mode(self):
        dev_list = pyiwd.dev_list()
        print("devices:", dev_list)
        station_list = [dev["Name"] for dev in dev_list \
            if dev["Mode"] == 'station']
        print("station_list:", station_list)





if __name__ == '__main__':
    unittest.main()


