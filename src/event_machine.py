from .dir_manager import DIR_MANAGER
from .model import MODEL
from .selection_handler import SELECTION
from .controller import Controller
from .tools import add_filters, get_filenames_from_selection

from gi.repository import Gio, GLib, Gtk

import logging
import gi
import gettext

gi.require_version("Gtk", "4.0")
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
            # Controller.reset_some_files()
            Controller.reset_all()
            self.is_real_selection = 1

    def on_reset_all_clicked(self, widget, action: Gio.Action):
        if self.is_real_selection == 1:
            self.is_real_selection = 0
            Controller.reset_all()
            self.is_real_selection = 1

    def on_about_clicked(self, widget, action: Gio.Action):
        if self.window is not None:
            self.window.id_about_window.show()

    def on_open_clicked(self, widget):
        self.is_real_selection = 0
        dialog = Gtk.FileDialog.new()
        dialog.set_title(_("Select a Folder"))
        dialog.set_modal(True)

        dialog.select_folder(self.window, None, self.on_open_folder_chooser)

        self.is_real_selection = 1

    def on_open_folder_chooser(self, dialog, result):
        try:
            gfile = dialog.select_folder_finish(result)
        except GLib.Error as err:
            logging.debug("Could not open folder: %s", err.message)
        else:
            Controller.change_directory(gfile.get_path())

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

            dialog = Gtk.FileDialog.new()
            dialog.set_title(_("Open a File"))
            dialog.set_modal(True)

            add_filters(dialog)

            dialog.open(self.window, None, self.on_open_image_chooser)

            self.is_real_selection = 1

    def on_open_image_chooser(self, dialog, result):
        try:
            gfile = dialog.open_finish(result)
        except GLib.Error as err:
            logging.debug("Could not open file: %s", err.message)
        else:
            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.update_modifications(name_files, "cover", gfile.get_path())
            Controller.update_view(name_files)

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

    def on_set_online_tags(self, widget, action: Gio.Action):
        if DIR_MANAGER.is_open_directory and self.is_real_selection == 1:
            self.is_real_selection = 0
            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.set_online_tags()

            if SELECTION.selection is not None:
                Controller.update_view(name_files)

            self.is_real_selection = 1


EVENT_MACHINE = EventMachine()
