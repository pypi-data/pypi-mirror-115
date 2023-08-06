#!/usr/bin/env python3

"""
pyiwd_combo: test functions of customzed comboboxtext
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies.

Usage: python -m unittest iwdgui.pyiwd_test

"""
import unittest

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from . import comboboxtext as comboboxtext

PRINT = False


"""
def braces2(func):

    def inner1(*args, **kwargs):
        print("[")
        func(*args, **kwargs)
        print("]")
  
    return inner1

@braces2
def hello2():
    print("hello")

hello2()

"""
class ComboBoxWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="ComboBox Example")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        combo = comboboxtext.ComboBoxText()
        combo.connect("changed", self.combo_changed)
        vbox.pack_start(combo, False, False, 0)

        countries = ["Austria", "Brazil", "Belgium", "France",
                     "Germany", "Switzerland", "United Kingdom",
                     "United States of America", "Uruguay"]

        combo.update_entries(countries)
        self.add(vbox)


    def combo_changed(self, widget):
        print("combo_changed")


class test_pyiwd_station(unittest.TestCase):

    def test_combo(self):

        win = ComboBoxWindow()
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()




if __name__ == '__main__':
    unittest.main()


