from gi import require_version
require_version('Gtk', '3.0')

from gi.repository import Gtk

class View:


    class __View:

        def __init__(self, tree_view, title, album, artist, genre):

            self.tree_view = tree_view
            self.title = title
            self.album = album
            self.artist = artist
            self.genre = genre

        def erase(self):
            self.genre.set_text("")
            self.album.set_text("")
            self.title.set_text("")
            self.artist.set_text("")

        def show(self,tagdico):
            self.genre.set_text(tagdico["genre"]["value"])
            self.album.set_text(tagdico["album"]["value"])
            self.title.set_text(tagdico["title"]["value"])
            self.artist.set_text(tagdico["artist"]["value"])

        def add_column(self, name):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(name, renderer, text=0)
            self.tree_view.append_column(column)



    __instance = None

    def __init__(self, tree_view, title, album, artist, genre):
        """ Virtually private constructor. """
        if View.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            View.__instance = View.__View(tree_view, title, album, artist, genre)


    @staticmethod
    def getInstance():
        """ Static access method. """
        if View.__instance == None:
            View(None,None,None,None,None)
        return View.__instance

