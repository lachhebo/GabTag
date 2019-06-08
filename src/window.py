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
from .Crawler_dir import Crawler_Dir
from .Crawler_modif import Crawler_Modif
from .data_crawler import Data_Crawler
from .treeview import TreeView


@GtkTemplate(ui='/com/github/lachhebo/Gabtag/window.ui')
class GabtagWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'GabtagWindow'


    ##HeaderBar
    id_popover_menu = GtkTemplate.Child()
    id_about_window = GtkTemplate.Child()

    ##Table
    tree_view_id = GtkTemplate.Child()
    liststore1 = GtkTemplate.Child()

    ## Tags
    id_album    = GtkTemplate.Child()
    id_artist   = GtkTemplate.Child()
    id_type     = GtkTemplate.Child()
    id_title    = GtkTemplate.Child()
    id_cover    = GtkTemplate.Child()
    id_year     = GtkTemplate.Child()
    id_track    = GtkTemplate.Child()

    ## Infos
    id_info_length  = GtkTemplate.Child()
    id_info_size    = GtkTemplate.Child()

    ##MusicBrainz

    id_album_mbz    = GtkTemplate.Child()
    id_artist_mbz   = GtkTemplate.Child()
    id_genre_mbz    = GtkTemplate.Child()
    id_title_mbz    = GtkTemplate.Child()
    id_cover_mbz    = GtkTemplate.Child()
    id_year_mbz     = GtkTemplate.Child()
    id_track_mbz    = GtkTemplate.Child()

    ## Pylyrics

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
            [self.id_title_mbz, self.id_album_mbz, self.id_artist_mbz, self.id_genre_mbz, self.id_cover_mbz, self.id_track_mbz, self.id_year_mbz],
            self.id_lyrics
        )

        view = View.getInstance()

        self.treeview = TreeView(self.liststore1,self.tree_view_id)

        self.data_crawler = Data_Crawler.getInstance()

        self.realselection = 0
        self.selectionned = None
        self.opened_directory = False

    @GtkTemplate.Callback
    def but_saved_cliqued(self, widget):
        if self.opened_directory == True :
            model = Model.getInstance()
            thread = Crawler_Modif(model.modification.copy(),self.liststore1,self.selectionned,0)
            #self.treeview.remove_crawled(model.modification.keys)
            model.save_modifications(self.selectionned)
            thread.start()


    @GtkTemplate.Callback
    def clicked_save_one(self,widget):
        if self.realselection == 1 :
            self.realselection = 0
            model = Model.getInstance()
            thread = Crawler_Modif(model.modification.copy(),self.liststore1,self.selectionned,1)
            model.save_one(self.selectionned)
            thread.start()
            self.realselection = 1

    @GtkTemplate.Callback
    def reset_one_clicked(self, widget):
        if self.realselection == 1 :
            self.realselection = 0
            model = Model.getInstance()
            model.reset_one(self.selectionned)
            self.realselection = 1

    @GtkTemplate.Callback
    def reset_all_clicked(self, widget):
        if self.realselection == 1 :
            self.realselection = 0
            model = Model.getInstance()
            model.reset_all(self.selectionned)
            self.realselection = 1

    @GtkTemplate.Callback
    def about_clicked(self,widget):
        self.id_about_window.run()
        self.id_about_window.hide()


    @GtkTemplate.Callback
    def open_clicked(self, widget):
        self.realselection = 0
        dialog = Gtk.FileChooserDialog("Please choose a folder", self,
        Gtk.FileChooserAction.SELECT_FOLDER,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()

        model = Model.getInstance()
        if response == Gtk.ResponseType.OK:
            self.opened_directory = True
            self.data_crawler.update_directory(dialog.get_filename())
            model.update_directory(dialog.get_filename(),self.liststore1)
            '''
            thread_mbz = threading.Thread(target = self.data_crawler.crawl_data, args=(dialog.get_filename(),self.liststore1)) #Writing data
            thread_mbz.start()
            '''
            thread = Crawler_Dir(model.directory,self.liststore1)
            thread.start()

            model.save_modifications(self.selectionned)


        dialog.destroy()

        # List mp3 file on the folder on the tree view :

        self.realselection = 1




    @GtkTemplate.Callback
    def on_menu_but_toggled(self, widget):
        pass


    @GtkTemplate.Callback
    def title_changed(self, widget):
        if self.realselection == 1 :
            self.realselection = 0
            model = Model.getInstance()
            model.update_modifications(self.selectionned,"title",widget.get_text())
            self.realselection = 1

    @GtkTemplate.Callback
    def artist_changed(self, widget):
        if self.realselection == 1 :
            self.realselection = 0
            model = Model.getInstance()
            model.update_modifications(self.selectionned,"artist",widget.get_text())
            self.realselection = 1

    @GtkTemplate.Callback
    def album_changed(self, widget):
        if self.realselection == 1 :
            self.realselection = 0
            model = Model.getInstance()
            model.update_modifications(self.selectionned,"album",widget.get_text())
            self.realselection = 1

    @GtkTemplate.Callback
    def type_changed(self, widget):
        if self.realselection == 1 :
            self.realselection = 0
            model = Model.getInstance()
            model.update_modifications(self.selectionned,"genre",widget.get_text())
            self.realselection = 1

    @GtkTemplate.Callback
    def track_changed(self,widget):
        if self.realselection == 1:
            self.realselection = 0
            model = Model.getInstance()
            model.update_modifications(self.selectionned,"track",widget.get_text())
            self.realselection = 1

    @GtkTemplate.Callback
    def year_changed(self,widget):
        if self.realselection == 1:
            self.realselection = 0
            model = Model.getInstance()
            model.update_modifications(self.selectionned,"year",widget.get_text())
            self.realselection = 1

    def add_filters(self, dialog):
        filter_png = Gtk.FileFilter()
        filter_png.set_name("Png")
        filter_png.add_mime_type("image/png")
        dialog.add_filter(filter_png)

        filter_jpeg = Gtk.FileFilter()
        filter_jpeg.set_name("jpeg")
        filter_jpeg.add_mime_type("image/jpeg")
        dialog.add_filter(filter_jpeg)



    @GtkTemplate.Callback
    def load_cover_clicked(self, widget):
        if self.realselection == 1:
            self.realselection = 0
            model = Model.getInstance()
            view = View.getInstance()

            dialog = Gtk.FileChooserDialog("Please choose a file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

            self.add_filters(dialog)

            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                file_cover = dialog.get_filename()
                model.update_modifications(self.selectionned,"cover",file_cover)
                model.update_view(self.selectionned)

            dialog.destroy()
            self.realselection = 1

    @GtkTemplate.Callback
    def selected_changed(self, selection):
        if self.realselection == 1 :
            self.realselection = 0
            self.selectionned = selection

            model = Model.getInstance()
            model.update_view(selection)

            self.realselection = 1


    @GtkTemplate.Callback
    def on_set_mbz(self, widget):
        if self.realselection == 1 :
            self.realselection = 0

            model = Model.getInstance()
            model.set_data_crawled(self.selectionned)
            model.update_view(self.selectionned)

            self.realselection = 1

    @GtkTemplate.Callback
    def on_rename_files(self, widget):
        if self.opened_directory == True :
            self.realselection = 0
            model = Model.getInstance()
            model.rename_files()
            model.update_list(self.liststore1)
            #thread_mbz = threading.Thread(target = self.data_crawler.crawl_data, args=(model.directory,self.liststore1)) #Writing data
            #thread_mbz.start()
            self.realselection = 1

        

    @GtkTemplate.Callback
    def on_set_online_tags(self,widget):
        if self.opened_directory == True :
            if self.realselection == 1 :
                self.realselection = 0
                model = Model.getInstance()

                model.set_online_tags()

                if self.selectionned != None :
                    model.update_view(self.selectionned)

                self.realselection = 1

    @GtkTemplate.Callback
    def on_set_lyrics(self,widget):
        if self.opened_directory == True :
            if self.realselection == 1 :
                self.realselection = 0

                model = Model.getInstance()
                model.set_data_lyrics(self.selectionned)

                self.realselection = 1
