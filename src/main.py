# main.py
#
# Copyright 2019 Ismaïl Lachheb
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

from .window_gtk import GabtagWindow

gi.require_version("Adw", "1")

from gi.repository import Adw, Gio, GLib, GObject  # noqa: E402


class Application(Adw.Application):

    app_id = GObject.Property(type=str)
    version = GObject.Property(type=str)
    devel = GObject.Property(type=bool, default=False)

    def __init__(self, app_id: str, version: str, devel: bool, *args, **kwargs):
        super().__init__(
            flags=Gio.ApplicationFlags.HANDLES_OPEN,
            *args,
            **kwargs
        )

        self.app_id = app_id
        self.version = version
        self.devel = devel

        GLib.set_application_name("GabTag")
        GLib.set_prgname(self.app_id)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = GabtagWindow(
                application=self,
                app_id=self.app_id,
                version=self.version,
                devel=self.devel,
            )
            win.set_default_icon_name(self.app_id)
        win.present()


def main(app_id, version, devel):
    app = Application(app_id, version, devel)
    return app.run(sys.argv)
