from src.controller import CONTROLER
from .tools import add_filters
from .treeview import TREE_VIEW
from .crawler_data import DATA_CRAWLER
from .crawler_modification import CrawlerModification
from .crawler_directory import CrawlerDirectory
from .view import VIEW, View
from .version import __version__
from .model import MODEL
from gi.repository import Gtk

import gi


gi.require_version("Gtk", "3.0")


@Gtk.Template(resource_path="/com/github/lachhebo/Gabtag/window.ui")
class GabtagWindow(Gtk.ApplicationWindow):
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

        TREE_VIEW.store = (self.liststore1,)
        TREE_VIEW.view = self.tree_view_id

        VIEW.tree_view_id = self.tree_view_id
        VIEW.id_title = self.id_title
        VIEW.id_album = self.id_album
        VIEW.id_artist = self.id_artist
        VIEW.id_type = self.id_type
        VIEW.id_cover = self.id_cover
        VIEW.id_track = self.id_track
        VIEW.id_year = self.id_year
        VIEW.id_info_length = self.id_info_length
        VIEW.id_info_size = self.id_info_size
        VIEW.id_title_mbz = self.id_title_mbz
        VIEW.id_album_mbz = self.id_album_mbz
        VIEW.id_artist_mbz = self.id_artist_mbz
        VIEW.id_genre_mbz = self.id_genre_mbz
        VIEW.id_cover_mbz = self.id_cover_mbz
        VIEW.id_track_mbz = self.id_track_mbz
        VIEW.id_year_mbz = self.id_year_mbz

        # Connect Buttons

        self.id_reset_all.connect("clicked", CONTROLER.reset_all_clicked)
        self.id_auto_tag.connect("clicked", CONTROLER.on_set_online_tags)
        self.id_about.connect("clicked", CONTROLER.about_clicked)
        self.but_open.connect("clicked", CONTROLER.open_clicked)
        self.but_save.connect("clicked", CONTROLER.but_saved_cliqued)
        self.id_load_cover.connect("clicked", CONTROLER.load_cover_clicked)
        self.id_reset_one.connect("clicked", CONTROLER.reset_all_clicked)
        self.id_save_one.connect("clicked", CONTROLER.clicked_save_one)
        self.id_setmbz_but.connect("clicked", CONTROLER.on_set_mbz)
        self.tree_selection_id.connect("changed", CONTROLER.selected_changed)
        self.id_album.connect("changed", CONTROLER.album_changed)
        self.id_artist.connect("changed", CONTROLER.artist_changed)
        self.id_type.connect("changed", CONTROLER.type_changed)
        self.id_title.connect("changed", CONTROLER.title_changed)
        self.id_year.connect("changed", CONTROLER.year_changed)
        self.id_track.connect("changed", CONTROLER.track_changed)

        CONTROLER.window = self
