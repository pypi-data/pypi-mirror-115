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

from . import wifi_channels

PRINT = False


loop = GLib.MainLoop()
main_context = GLib.MainLoop.get_context(loop)


class test_wifi_channels(unittest.TestCase):

    def test_dictionary_test(self):
        channel = wifi_channels.WIFI_ALL_CHANNELS[6395]

    def test_function_test(self):
        channel = wifi_channels.wifi_channel(6395)

    def test_bad_freq(self):
        channel =  wifi_channels.wifi_channel(12)





if __name__ == '__main__':
    unittest.main()


