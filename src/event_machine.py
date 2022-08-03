from .dir_manager import DIR_MANAGER
from .model import MODEL
from .selection_handler import SELECTION
from .controller import Controller
from .tools import add_filters, get_filenames_from_selection
from .version import __version__

from gi.repository import Gtk

import gi
import gettext

gi.require_version("Gtk", "3.0")
_ = gettext.gettext


class EventMachine:
    def __init__(self) -> None:
        self.window = None
        self.is_real_selection = 0

    def on_but_saved_clicked(self, widget):
        if DIR_MANAGER.is_open_directory:
            Controller.crawl_thread_modification()

    def on_clicked_save_one(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            Controller.save_some_files()
            self.is_real_selection = 1

    def on_reset_one_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            Controller.reset_some_files()
            self.is_real_selection = 1

    def on_reset_all_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            Controller.reset_all()
            self.is_real_selection = 1

    def on_about_clicked(self, widget):
        self.window.id_about_window.set_version(__version__)
        self.window.id_about_window.run()
        self.window.id_about_window.hide()

    def on_open_clicked(self, widget):
        self.is_real_selection = 0
        dialog = Gtk.FileChooserNative.new(
            _("Select Folder"),
            self.window,
            Gtk.FileChooserAction.SELECT_FOLDER,
            _("Select"),
            _("Cancel")
        )

        response = dialog.run()

        if response == Gtk.ResponseType.ACCEPT:
            Controller.change_directory(dialog.get_filename())

        dialog.destroy()

        self.is_real_selection = 1

    def on_menu_but_toggled(self, widget):
        pass

    def on_title_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            Controller.react_to_user_modif("title", widget.get_text())
            self.is_real_selection = 1

    def on_artist_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            Controller.react_to_user_modif("artist", widget.get_text())
            self.is_real_selection = 1

    def on_album_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            Controller.react_to_user_modif("album", widget.get_text())
            self.is_real_selection = 1

    def on_type_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            Controller.react_to_user_modif("genre", widget.get_text())
            self.is_real_selection = 1

    def on_track_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            Controller.react_to_user_modif("track", widget.get_text())
            self.is_real_selection = 1

    def on_year_changed(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            Controller.react_to_user_modif("year", widget.get_text())
            self.is_real_selection = 1

    def on_load_cover_clicked(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0

            dialog = Gtk.FileChooserNative.new(
                _("Open File"),
                self.window,
                Gtk.FileChooserAction.OPEN,
                _("Open"),
                _("Cancel")
            )

            add_filters(dialog)
            response = dialog.run()

            if response == Gtk.ResponseType.ACCEPT:
                file_cover = dialog.get_filename()
                name_files = get_filenames_from_selection(SELECTION.selection)
                MODEL.update_modifications(name_files, "cover", file_cover)
                Controller.update_view(name_files)

            dialog.destroy()
            self.is_real_selection = 1

    def on_selected_changed(self, selection):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            self.update_selection(selection)
            self.is_real_selection = 1

    def update_selection(self, selection):
        SELECTION.selection = selection
        name_files = get_filenames_from_selection(SELECTION.selection)
        Controller.update_view(name_files)

    def on_set_mbz(self, widget):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.set_data_crawled(name_files)
            Controller.update_view(name_files)
            self.is_real_selection = 1

    def on_set_online_tags(self, widget):
        if DIR_MANAGER.is_open_directory and self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.set_online_tags()

            if SELECTION.selection is not None:
                Controller.update_view(name_files)

            self.is_real_selection = 1


EVENT_MACHINE = EventMachine()
