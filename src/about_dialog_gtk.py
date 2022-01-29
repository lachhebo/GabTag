import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk  # noqa: E402


@Gtk.Template(resource_path='/com/github/lachhebo/Gabtag/about_dialog.ui')
class GabTagAboutDialog(Gtk.AboutDialog):
    __gtype_name__ = 'GabTagAboutDialog'

    def __init__(self, parent, version):
        super().__init__()
        self.set_transient_for(parent)
        self.set_version(version)
