import logging
from gi.repository import Pango
from gi.repository import Gio, Gtk
import gi
gi.require_version('Gtk', '3.0')


class TreeView:

    class __TreeView:

        def __init__(self, store, view):
            self.store = store
            self.view = view

            if self.store != None and self.view != None:
                self.view.set_model(self.store)

                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(
                    "Name", renderer, text=0, weight=2, weight_set=True)
                self.view.append_column(column)

                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(
                    "Data Crawled", renderer, text=1, weight=2, weight_set=True)
                self.view.append_column(column)

        def remove_crawled(self, namefiles):
            finded = -1
            i = 0

            for filename in namefiles:
                for row in self.store:
                    if row[0] == filename:
                        finded = i
                    else:
                        i = i+1

                if finded != -1:
                    path = Gtk.TreePath(finded)
                    listiter = self.store.get_iter(path)
                    self.store.set_value(listiter, 1, "No")

        def add_crawled(self, namefiles):
            finded = -1
            i = 0

            for filename in namefiles:
                for row in self.store:
                    if row[0] == filename:
                        finded = i
                    else:
                        i = i+1

                if finded != -1:
                    path = Gtk.TreePath(finded)
                    listiter = self.store.get_iter(path)
                    self.store.set_value(listiter, 1, "Yes")

        def add_bold_font(self, namefiles):

            finded = -1
            i = 0

            for filename in namefiles:
                for row in self.store:
                    if row[0] == filename:
                        finded = i
                    else:
                        i = i+1

                if finded != -1:
                    path = Gtk.TreePath(finded)
                    listiter = self.store.get_iter(path)
                    self.store.set_value(listiter, 2, 700)

        def remove_bold_font(self, namefiles):

            finded = -1
            i = 0

            for filename in namefiles:
                for row in self.store:
                    if row[0] == filename:
                        finded = i
                    else:
                        i = i+1

                if finded != -1:
                    path = Gtk.TreePath(finded)
                    listiter = self.store.get_iter(path)
                    self.store.set_value(listiter, 2, 400)

    __instance = None

    def __init__(self, store, view):
        """ Virtually private constructor. """
        if TreeView.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            TreeView.__instance = TreeView.__TreeView(store, view)

    @staticmethod
    def getInstance():
        """ Static access method. """
        if TreeView.__instance == None:
            TreeView(None, None)
        return TreeView.__instance
