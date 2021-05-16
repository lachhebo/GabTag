# main.py
#
# Copyright 2019 Ismaël Lachheb
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
import sys

from .window import GabtagWindow

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GLib  # noqa: E402


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.github.lachhebo.Gabtag',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name(('GabTag'))
        GLib.set_prgname('com.github.lachhebo.Gabtag')

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = GabtagWindow(application=self)
            win.set_default_icon_name(self.props.application_id)
        win.present()


def main(version):
    app = Application()
    return app.run(sys.argv)
