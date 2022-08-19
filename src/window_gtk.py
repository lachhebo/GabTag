from .event_machine import EVENT_MACHINE
from .treeview import TREE_VIEW
from .view import VIEW

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio, GObject, Gtk  # noqa: E402


@Gtk.Template(resource_path="/com/github/lachhebo/Gabtag/window.ui")
class GabtagWindow(Adw.ApplicationWindow):
    __gtype_name__ = "GabtagWindow"

    app_id = GObject.Property(type=str)
    version = GObject.Property(type=str)
    devel = GObject.Property(type=bool, default=False)

    # HeaderBar
    id_about_window = Gtk.Template.Child()

    # Table
    tree_view_id = Gtk.Template.Child()
    liststore1 = Gtk.Template.Child()

    carousel = Gtk.Template.Child()

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
    but_open_fold = Gtk.Template.Child()
    but_save = Gtk.Template.Child()
    id_load_cover = Gtk.Template.Child()
    edit_tags_but = Gtk.Template.Child()
    set_tags_but = Gtk.Template.Child()
    id_reset_one = Gtk.Template.Child()
    id_save_one = Gtk.Template.Child()
    id_setmbz_but = Gtk.Template.Child()
    tree_selection_id = Gtk.Template.Child()

    def __init__(self, app_id, version, devel, **kwargs):
        super().__init__(**kwargs)

        if devel:
            self.add_css_class("devel")

        self.set_default_icon_name(app_id)
        self.id_about_window.set_application_icon(app_id)
        self.id_about_window.set_version(version)

        TREE_VIEW.store = self.liststore1
        TREE_VIEW.view = self.tree_view_id
        TREE_VIEW.add_columns()

        VIEW.tree_view = self.tree_view_id
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

        self.but_open.connect("clicked", EVENT_MACHINE.on_open_clicked)
        self.but_open_fold.connect("clicked", EVENT_MACHINE.on_open_clicked)
        self.but_save.connect("clicked", EVENT_MACHINE.on_but_saved_clicked)

        reset_all = Gio.SimpleAction.new("reset-all", None)
        reset_all.connect("activate", EVENT_MACHINE.on_reset_all_clicked)
        self.add_action(reset_all)

        set_online_tags = Gio.SimpleAction.new("set-online-tags", None)
        set_online_tags.connect("activate", EVENT_MACHINE.on_set_online_tags)
        self.add_action(set_online_tags)

        about = Gio.SimpleAction.new("about", None)
        about.connect("activate", EVENT_MACHINE.on_about_clicked)
        self.add_action(about)

        self.id_load_cover.connect("clicked", EVENT_MACHINE.on_load_cover_clicked)
        self.edit_tags_but.connect("clicked", EVENT_MACHINE.on_switch_page_clicked)
        self.set_tags_but.connect("clicked", EVENT_MACHINE.on_switch_page_clicked)
        self.id_reset_one.connect("clicked", EVENT_MACHINE.on_reset_one_clicked)
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
