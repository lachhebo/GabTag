from .event_machine import EVENT_MACHINE
from .treeview import TREE_VIEW
from .view import VIEW

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Handy", "1")

from gi.repository import Gtk, Handy  # noqa: E402


@Gtk.Template(resource_path="/com/github/lachhebo/Gabtag/window.ui")
class GabtagWindow(Handy.ApplicationWindow):
    __gtype_name__ = "GabtagWindow"

    # HeaderBar
    id_popover_menu = Gtk.Template.Child()
    id_about_window = Gtk.Template.Child()

    # Table
    tree_view_id = Gtk.Template.Child()
    liststore1 = Gtk.Template.Child()

    # Tags
    id_album = Gtk.Template.Child()
    id_artist = Gtk.Template.Child()
    id_type = Gtk.Template.Child()
    id_title = Gtk.Template.Child()
    id_cover = Gtk.Template.Child()
    id_year = Gtk.Template.Child()
    id_track = Gtk.Template.Child()

    # Infos
    id_info_length = Gtk.Template.Child()
    id_info_size = Gtk.Template.Child()

    # MusicBrainz

    id_album_mbz = Gtk.Template.Child()
    id_artist_mbz = Gtk.Template.Child()
    id_genre_mbz = Gtk.Template.Child()
    id_title_mbz = Gtk.Template.Child()
    id_cover_mbz = Gtk.Template.Child()
    id_year_mbz = Gtk.Template.Child()
    id_track_mbz = Gtk.Template.Child()

    # Buttons

    but_open = Gtk.Template.Child()
    id_reset_all = Gtk.Template.Child()
    id_auto_tag = Gtk.Template.Child()
    id_about = Gtk.Template.Child()
    but_save = Gtk.Template.Child()
    id_load_cover = Gtk.Template.Child()
    id_reset_one = Gtk.Template.Child()
    id_save_one = Gtk.Template.Child()
    id_setmbz_but = Gtk.Template.Child()
    tree_selection_id = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        TREE_VIEW.store = self.liststore1
        TREE_VIEW.view = self.tree_view_id
        TREE_VIEW.add_columns()

        VIEW.tree_view_id = self.tree_view_id
        VIEW.title = self.id_title
        VIEW.album = self.id_album
        VIEW.artist = self.id_artist
        VIEW.genre = self.id_type
        VIEW.cover = self.id_cover
        VIEW.track = self.id_track
        VIEW.year = self.id_year
        VIEW.length = self.id_info_length
        VIEW.size = self.id_info_size
        VIEW.title_mbz = self.id_title_mbz
        VIEW.album_mbz = self.id_album_mbz
        VIEW.artist_mbz = self.id_artist_mbz
        VIEW.genre_mbz = self.id_genre_mbz
        VIEW.cover_mbz = self.id_cover_mbz
        VIEW.track_mbz = self.id_track_mbz
        VIEW.year_mbz = self.id_year_mbz

        # Connect Buttons

        self.id_reset_all.connect("clicked", EVENT_MACHINE.on_reset_all_clicked)
        self.id_auto_tag.connect("clicked", EVENT_MACHINE.on_set_online_tags)
        self.id_about.connect("clicked", EVENT_MACHINE.on_about_clicked)
        self.but_open.connect("clicked", EVENT_MACHINE.on_open_clicked)
        self.but_save.connect("clicked", EVENT_MACHINE.on_but_saved_clicked)
        self.id_load_cover.connect("clicked", EVENT_MACHINE.on_load_cover_clicked)
        self.id_reset_one.connect("clicked", EVENT_MACHINE.on_reset_all_clicked)
        self.id_save_one.connect("clicked", EVENT_MACHINE.on_clicked_save_one)
        self.id_setmbz_but.connect("clicked", EVENT_MACHINE.on_set_mbz)
        self.tree_selection_id.connect("changed", EVENT_MACHINE.on_selected_changed)
        self.id_album.connect("changed", EVENT_MACHINE.on_album_changed)
        self.id_artist.connect("changed", EVENT_MACHINE.on_artist_changed)
        self.id_type.connect("changed", EVENT_MACHINE.on_type_changed)
        self.id_title.connect("changed", EVENT_MACHINE.on_title_changed)
        self.id_year.connect("changed", EVENT_MACHINE.on_year_changed)
        self.id_track.connect("changed", EVENT_MACHINE.on_track_changed)

        EVENT_MACHINE.window = self
