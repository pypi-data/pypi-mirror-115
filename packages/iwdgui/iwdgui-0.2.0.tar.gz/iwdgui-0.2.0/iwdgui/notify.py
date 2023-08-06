#!/usr/bin/python3
"""
notify: deskop notifications using D-BUS
(c) 2021 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

from .dbus import session_bus as bus
import dbus

try:
    from .icon import icon_path
except:
    from icon import icon_path

NOTIFY_PATH = "/org/freedesktop/Notifications"
NOTIFY_IF = "org.freedesktop.Notifications"
ICON_RESOLUTION = 96

class Notify():
    def __init__(self):
        "Class init, creates the dbus interface"
        self.id = 0
        self.notify_if = dbus.Interface(
            bus.get_object(NOTIFY_IF, NOTIFY_PATH), NOTIFY_IF)

    def _msg(self, summary, body, app_name="Iwdgui", replaces_id=0,
             app_icon="iwdgui", actions=[], hints = {"urgency": 1},
             expire_timeout=5000):
        "Internal notification message function"
        app_icon_path = icon_path(iconname=app_icon, res=ICON_RESOLUTION)
        return self.notify_if.Notify(app_name, replaces_id,
                                     app_icon_path, summary, body,
                                     actions, hints, expire_timeout)

    def msg(self, body):
        "Iwd specific function, only requiring a body"
        self.id = self._msg("IWD", body, replaces_id=self.id)
