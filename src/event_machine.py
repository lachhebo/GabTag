from .dir_manager import DIR_MANAGER
from .model import MODEL
from .selection_handler import SELECTION
from .controller import Controller
from .tools import add_filters, get_filenames_from_selection

import gi
import gettext

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio, Gtk  # noqa: E402

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
        dialog = Gtk.FileChooserDialog(
            title=_("Select a Folder"),
            transient_for=self.window,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(_("_Open"), Gtk.ResponseType.OK)
        dialog.add_buttons(_("_Cancel"), Gtk.ResponseType.CANCEL)
        dialog.set_default_response(Gtk.ResponseType.OK)
        dialog.set_modal(True)

        dialog.connect("response", self.on_open_folder_chooser)

        dialog.show()

        self.is_real_selection = 1

    def on_open_folder_chooser(self, dialog, response):
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            Controller.change_directory(dialog.get_file().get_path())

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

            dialog = Gtk.FileChooserDialog(
                title=_("Open a File"),
                transient_for=self.window,
                action=Gtk.FileChooserAction.OPEN,
            )
            dialog.add_buttons(_("_Open"), Gtk.ResponseType.OK)
            dialog.add_buttons(_("_Cancel"), Gtk.ResponseType.CANCEL)
            dialog.set_default_response(Gtk.ResponseType.OK)
            dialog.set_modal(True)

            add_filters(dialog)

            dialog.connect("response", self.on_open_image_chooser)

            dialog.show()

            self.is_real_selection = 1

    def on_open_image_chooser(self, dialog, response):
        dialog.destroy()

        if response == Gtk.ResponseType.OK:
            file_cover = dialog.get_file().get_path()

            name_files = get_filenames_from_selection(SELECTION.selection)
            MODEL.update_modifications(name_files, "cover", file_cover)
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

    def on_switch_page_clicked(self, widget):
        self.is_real_selection = 0

        current_page = Adw.Carousel.get_position(self.window.carousel)
        new_page = self.window.carousel.get_nth_page((current_page + 1.0) % 2)

        self.window.carousel.scroll_to(new_page, True)

        self.is_real_selection = 1


EVENT_MACHINE = EventMachine()
