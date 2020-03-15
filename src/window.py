# window.py
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
from .tools import add_filters
from .treeview import TreeView
from .crawler_data import DataCrawler
from .crawler_modification import CrawlerModification
from .crawler_directory import CrawlerDirectory
from .view import View
from .model import Model
from .gi_composites import GtkTemplate
from gi.repository import Gio, Gtk
import gi
gi.require_version('Gtk', '3.0')


@GtkTemplate(ui='/com/github/lachhebo/Gabtag/window.ui')
class GabtagWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'GabtagWindow'

    # HeaderBar
    id_popover_menu = GtkTemplate.Child()
    id_about_window = GtkTemplate.Child()

    # Table
    tree_view_id = GtkTemplate.Child()
    liststore1 = GtkTemplate.Child()

    # Tags
    id_album = GtkTemplate.Child()
    id_artist = GtkTemplate.Child()
    id_type = GtkTemplate.Child()
    id_title = GtkTemplate.Child()
    id_cover = GtkTemplate.Child()
    id_year = GtkTemplate.Child()
    id_track = GtkTemplate.Child()

    # Infos
    id_info_length = GtkTemplate.Child()
    id_info_size = GtkTemplate.Child()

    # MusicBrainz

    id_album_mbz = GtkTemplate.Child()
    id_artist_mbz = GtkTemplate.Child()
    id_genre_mbz = GtkTemplate.Child()
    id_title_mbz = GtkTemplate.Child()
    id_cover_mbz = GtkTemplate.Child()
    id_year_mbz = GtkTemplate.Child()
    id_track_mbz = GtkTemplate.Child()

    # Pylyrics

    id_lyrics = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        View(
            self.tree_view_id,
            self.id_title,
            self.id_album,
            self.id_artist,
            self.id_type,
            self.id_cover,
            self.id_track,
            self.id_year,
            self.id_info_length,
            self.id_info_size,
            [self.id_title_mbz, self.id_album_mbz, self.id_artist_mbz,
                self.id_genre_mbz, self.id_cover_mbz, self.id_track_mbz, self.id_year_mbz],
            self.id_lyrics
        )

        view = View.get_instance()

        self.tree_view = TreeView(self.liststore1, self.tree_view_id)

        self.data_crawler = DataCrawler.get_instance()

        self.is_real_selection = 0
        self.selectioned = None
        self.is_opened_directory = False

    @GtkTemplate.Callback
    def but_saved_cliqued(self, widget):
        if self.is_opened_directory == True:
            model = Model.get_instance()
            thread = CrawlerModification(
                model.modification.copy(), self.liststore1, self.selectioned, 0)
            model.save_modifications(self.selectioned)
            thread.start()

    @GtkTemplate.Callback
    def clicked_save_one(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = Model.get_instance()
            thread = CrawlerModification(
                model.modification.copy(), self.liststore1, self.selectioned, 1)
            model.save_one(self.selectioned)
            thread.start()
            self.is_real_selection = 1

    @GtkTemplate.Callback
    def reset_one_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = Model.get_instance()
            model.reset_one(self.selectioned)
            self.is_real_selection = 1

    @GtkTemplate.Callback
    def reset_all_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = Model.get_instance()
            model.reset_all(self.selectioned)
            self.is_real_selection = 1

    @GtkTemplate.Callback
    def about_clicked(self, widget):
        self.id_about_window.run()
        self.id_about_window.hide()

    @GtkTemplate.Callback
    def open_clicked(self, widget):
        self.is_real_selection = 0
        dialog = Gtk.FileChooserDialog('Please choose a folder', self,
                                       Gtk.FileChooserAction.SELECT_FOLDER,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        'Select', Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()

        model = Model.get_instance()
        if response == Gtk.ResponseType.OK:
            self.is_opened_directory = True
            model.view.erase()
            self.data_crawler.update_directory(dialog.get_filename())
            model.update_directory(dialog.get_filename(), self.liststore1)
            thread = CrawlerDirectory(model.directory, self.liststore1)
            thread.start()

        dialog.destroy()

        # List mp3 file on the folder on the tree view :

        self.is_real_selection = 1

    @GtkTemplate.Callback
    def on_menu_but_toggled(self, widget):
        pass

    @GtkTemplate.Callback
    def title_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = Model.get_instance()
            model.update_modifications(
                self.selectioned, 'title', widget.get_text())
            self.is_real_selection = 1

    @GtkTemplate.Callback
    def artist_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = Model.get_instance()
            model.update_modifications(
                self.selectioned, 'artist', widget.get_text())
            self.is_real_selection = 1

    @GtkTemplate.Callback
    def album_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = Model.get_instance()
            model.update_modifications(
                self.selectioned, 'album', widget.get_text())
            self.is_real_selection = 1

    @GtkTemplate.Callback
    def type_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = Model.get_instance()
            model.update_modifications(
                self.selectioned, 'genre', widget.get_text())
            self.is_real_selection = 1

    @GtkTemplate.Callback
    def track_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = Model.get_instance()
            model.update_modifications(
                self.selectioned, 'track', widget.get_text())
            self.is_real_selection = 1

    @GtkTemplate.Callback
    def year_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = Model.get_instance()
            model.update_modifications(
                self.selectioned, 'year', widget.get_text())
            self.is_real_selection = 1


    @GtkTemplate.Callback
    def load_cover_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = Model.get_instance()

            dialog = Gtk.FileChooserDialog('Please choose a file', self,
                                           Gtk.FileChooserAction.OPEN,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

            add_filters(dialog)

            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                file_cover = dialog.get_filename()
                model.update_modifications(
                    self.selectioned, 'cover', file_cover)
                model.update_view(self.selectioned)

            dialog.destroy()
            self.is_real_selection = 1

    @GtkTemplate.Callback
    def selected_changed(self, selection):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            self.selectioned = selection

            model = Model.get_instance()
            model.update_view(selection)

            self.is_real_selection = 1

    @GtkTemplate.Callback
    def on_set_mbz(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0

            model = Model.get_instance()
            model.set_data_crawled(self.selectioned)
            model.update_view(self.selectioned)

            self.is_real_selection = 1

    @GtkTemplate.Callback
    def on_rename_files(self, widget):
        if self.is_opened_directory:
            self.is_real_selection = 0
            model = Model.get_instance()
            model.rename_files()
            model.update_list(self.liststore1)
            self.is_real_selection = 1

    @GtkTemplate.Callback
    def on_set_online_tags(self, widget):
        if self.is_opened_directory:
            if self.is_real_selection == 1:
                self.is_real_selection = 0
                model = Model.get_instance()

                model.set_online_tags()

                if self.selectioned is not None:
                    model.update_view(self.selectioned)

                self.is_real_selection = 1

    @GtkTemplate.Callback
    def on_set_lyrics(self, widget):
        if self.is_opened_directory:
            if self.is_real_selection == 1:
                self.is_real_selection = 0

                model = Model.get_instance()
                model.set_data_lyrics(self.selectioned)

                self.is_real_selection = 1

