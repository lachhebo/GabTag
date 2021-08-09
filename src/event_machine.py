from .crawler_modification import CrawlerModification
from .dir_manager import DIR_MANAGER
from .model import MODEL
from .selection_handler import SELECTION
from .treeview import TREE_VIEW
from .controller import CONTROLLER
from .crawler_directory import CrawlerDirectory
from .tools import add_filters, get_filenames_from_selection
from .version import __version__

from gi.repository import Gtk

import gi

from .view import VIEW

gi.require_version("Gtk", "3.0")


class EventMachine:
    def __init__(self) -> None:
        self.window = None
        self.is_real_selection: bool = 0

    def on_but_saved_clicked(self, widget):
        if DIR_MANAGER.is_opened_directory:

            thread = CrawlerModification(MODEL.modification.copy(), TREE_VIEW.store)
            MODEL.save_modifications(TREE_VIEW)
            thread.start()

    def on_clicked_save_one(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            thread = CrawlerModification(MODEL.modification.copy(), name_files)
            MODEL.save_modifications(TREE_VIEW, name_files=name_files)
            thread.start()
            self.is_real_selection = 1

    def on_reset_one_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            CONTROLLER.reset_one(name_files)
            self.is_real_selection = 1

    def on_reset_all_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            CONTROLLER.reset_all()
            self.is_real_selection = 1

    def on_about_clicked(self, widget):
        self.window.id_about_window.set_version(__version__)
        self.window.id_about_window.run()
        self.window.id_about_window.hide()

    def on_open_clicked(self, widget):
        self.is_real_selection = 0
        dialog = Gtk.FileChooserDialog(
            "Please choose a folder",
            self.window,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK),
        )
        dialog.set_default_size(800, 400)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            VIEW.erase()

            CONTROLLER.update_directory(dialog.get_filename())
            thread = CrawlerDirectory(DIR_MANAGER.directory)
            thread.start()

        dialog.destroy()

        self.is_real_selection = 1

    def on_menu_but_toggled(self, widget):
        pass

    def on_title_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.update_modifications(name_files, "title", widget.get_text())
            self.is_real_selection = 1

    def on_artist_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.update_modifications(name_files, "artist", widget.get_text())
            TREE_VIEW.manage_bold_font(name_files)
            self.is_real_selection = 1

    def on_album_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.update_modifications(name_files, "album", widget.get_text())
            TREE_VIEW.manage_bold_font(name_files)
            self.is_real_selection = 1

    def on_type_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.update_modifications(name_files, "genre", widget.get_text())
            TREE_VIEW.manage_bold_font(name_files)
            self.is_real_selection = 1

    def on_track_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.update_modifications(name_files, "track", widget.get_text())
            TREE_VIEW.manage_bold_font(name_files)
            self.is_real_selection = 1

    def on_year_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.update_modifications(name_files, "year", widget.get_text())
            TREE_VIEW.manage_bold_font(name_files)
            self.is_real_selection = 1

    def on_load_cover_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0

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
                name_files = get_filenames_from_selection(SELECTION.selection)
                MODEL.update_modifications(name_files, "cover", file_cover)
                CONTROLLER.update_view(name_files)

            dialog.destroy()
            self.is_real_selection = 1

    def on_selected_changed(self, selection):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            SELECTION.selection = selection
            name_files = get_filenames_from_selection(SELECTION.selection)

            CONTROLLER.update_view(name_files)

            self.is_real_selection = 1

    def on_set_mbz(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.set_data_crawled(name_files)
            CONTROLLER.update_view(name_files)
            self.is_real_selection = 1

    def on_set_online_tags(self, widget):
        if DIR_MANAGER.is_opened_directory:
            if self.is_real_selection == 1:
                self.is_real_selection = 0
                name_files = get_filenames_from_selection(SELECTION.selection)

                MODEL.set_online_tags()

                if self.selectioned is not None:
                    CONTROLLER.update_view(name_files)

                self.is_real_selection = 1


EVENT_MACHINE = EventMachine()
