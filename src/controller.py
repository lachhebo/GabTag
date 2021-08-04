from src.crawler_data import DATA_CRAWLER
from .model import MODEL
from .version import __version__
from .tools import add_filters
from .crawler_directory import CrawlerDirectory
from .crawler_modification import CrawlerModification

from gi.repository import Gtk

import gi


gi.require_version("Gtk", "3.0")



class Controller:

    def __init__(self) -> None:
        self.window = None
        self.is_real_selection: bool = 0
        self.data_crawler = DATA_CRAWLER
        self.selectioned = None
        self.is_opened_directory = False

    def but_saved_cliqued(self, widget):
        if self.is_opened_directory:
            model = MODEL
            thread = CrawlerModification(model.modification.copy(),
                                            self.liststore1,
                                            self.selectioned,
                                            0)
            model.save_modifications(self.selectioned)
            thread.start()

    def clicked_save_one(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = MODEL
            thread = CrawlerModification(model.modification.copy(),
                                         self.liststore1,
                                         self.selectioned,
                                         1)
            model.save_one(self.selectioned)
            thread.start()
            self.is_real_selection = 1

    def reset_one_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = MODEL
            model.reset_one(self.selectioned)
            self.is_real_selection = 1

    def reset_all_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = MODEL
            model.reset_all(self.selectioned)
            self.is_real_selection = 1

    def about_clicked(self, widget):
        self.id_about_window.set_version(__version__)
        self.id_about_window.run()
        self.id_about_window.hide()

    def open_clicked(self, widget):
        self.is_real_selection = 0
        dialog = Gtk.FileChooserDialog(
            "Please choose a folder",
            self,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK),
        )
        dialog.set_default_size(800, 400)

        response = dialog.run()

        model = MODEL
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

    def on_menu_but_toggled(self, widget):
        pass

    def title_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = MODEL
            model.update_modifications(self.selectioned, "title", widget.get_text())
            self.is_real_selection = 1

    def artist_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = MODEL
            model.update_modifications(self.selectioned, "artist", widget.get_text())
            self.is_real_selection = 1

    def album_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = MODEL
            model.update_modifications(self.selectioned, "album", widget.get_text())
            self.is_real_selection = 1

    def type_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = MODEL
            model.update_modifications(self.selectioned, "genre", widget.get_text())
            self.is_real_selection = 1

    def track_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = MODEL
            model.update_modifications(self.selectioned, "track", widget.get_text())
            self.is_real_selection = 1

    def year_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = MODEL
            model.update_modifications(self.selectioned, "year", widget.get_text())
            self.is_real_selection = 1

    def load_cover_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            model = MODEL

            dialog = Gtk.FileChooserDialog(
                "Please choose a file",
                self.window,
                Gtk.FileChooserAction.OPEN,
                (
                    Gtk.STOCK_CANCEL,
                    Gtk.ResponseType.CANCEL,
                    Gtk.STOCK_OPEN,
                    Gtk.ResponseType.OK,
                ),
            )

            add_filters(dialog)
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                file_cover = dialog.get_filename()
                model.update_modifications(self.selectioned, "cover", file_cover)
                model.update_view(self.selectioned)

            dialog.destroy()
            self.is_real_selection = 1

    def selected_changed(self, selection):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            self.selectioned = selection

            model = MODEL
            model.update_view(selection)

            self.is_real_selection = 1

    def on_set_mbz(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0

            model = MODEL
            model.set_data_crawled(self.selectioned)
            model.update_view(self.selectioned)

            self.is_real_selection = 1

    def on_set_online_tags(self, widget):
        if self.is_opened_directory:
            if self.is_real_selection == 1:
                self.is_real_selection = 0
                model = MODEL

                model.set_online_tags()

                if self.selectioned is not None:
                    model.update_view(self.selectioned)

                self.is_real_selection = 1



CONTROLER = Controller()