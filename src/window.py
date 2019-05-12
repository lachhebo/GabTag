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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk

from .gi_composites import GtkTemplate

from .model import Model
from .view import View

@GtkTemplate(ui='/org/gnome/Gabtag/window.ui')
class GabtagWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'GabtagWindow'

    tree_view_id = GtkTemplate.Child()
    liststore1 = GtkTemplate.Child()
    id_album = GtkTemplate.Child()
    id_artist = GtkTemplate.Child()
    id_type = GtkTemplate.Child()
    id_title  = GtkTemplate.Child()
    id_cover = GtkTemplate.Child()
    id_popover_menu = GtkTemplate.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        View(self.tree_view_id, self.id_title, self.id_album, self.id_artist, self.id_type, self.id_cover)

        view = View.getInstance()

        self.tree_view_id.set_model(self.liststore1)

        view.add_column("Title")

        self.realselection = 0
        self.selectionned = None


    @GtkTemplate.Callback
    def but_saved_cliqued(self, widget):
        model = Model.getInstance()
        model.save_modifications()


    @GtkTemplate.Callback
    def open_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
        Gtk.FileChooserAction.SELECT_FOLDER,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()

        model = Model.getInstance()
        if response == Gtk.ResponseType.OK:
            model.update_directory(dialog.get_filename())

        dialog.destroy()

        # List mp3 file on the folder on the tree view :

        tree_view_id = GtkTemplate.Child()
        liststore1 = GtkTemplate.Child()

        model.update_list(self.liststore1)



    @GtkTemplate.Callback
    def on_menu_but_toggled(self, widget):
        print("The button menu was clicked")


    @GtkTemplate.Callback
    def title_changed(self, widget):
        if self.realselection == 1 :
            model = Model.getInstance()
            model.update_modifications(self.selectionned,"title",widget.get_text())

    @GtkTemplate.Callback
    def artist_changed(self, widget):
        if self.realselection == 1 :
            model = Model.getInstance()
            model.update_modifications(self.selectionned,"artist",widget.get_text())

    @GtkTemplate.Callback
    def album_changed(self, widget):
        if self.realselection == 1 :
            model = Model.getInstance()
            model.update_modifications(self.selectionned,"album",widget.get_text())

    @GtkTemplate.Callback
    def type_changed(self, widget):
        if self.realselection == 1 :
            model = Model.getInstance()
            model.update_modifications(self.selectionned,"genre",widget.get_text())

    @GtkTemplate.Callback
    def load_cover_clicked(self, widget):
        if self.realselection == 1:
            model = Model.getInstance()

            dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

            #self.add_filters(dialog)

            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                file_cover = dialog.get_filename()
                print("La COVER : ",file_cover)
                model.update_modifications(self.selectionned,"cover",file_cover)

            dialog.destroy()


    @GtkTemplate.Callback
    def selected_changed(self, selection):

        self.realselection = 0
        self.selectionned = selection

        model = Model.getInstance()
        model.update_view(selection)

        self.realselection = 1


