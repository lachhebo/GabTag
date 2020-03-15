import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk


class TreeView:

    class __TreeView:

        def __init__(self, store, view):
            self.store = store
            self.view = view

            if self.store is not None and self.view is not None:
                self.view.set_model(self.store)

                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(
                    'Name', renderer, text=0, weight=2, weight_set=True)
                self.view.append_column(column)

                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(
                    'Data Crawled', renderer, text=1, weight=2, weight_set=True)
                self.view.append_column(column)

        def remove_crawled(self, name_files):
            line_number = -1
            i = 0

            for filename in name_files:
                for row in self.store:
                    if row[0] == filename:
                        line_number = i
                    else:
                        i = i+1

                if line_number != -1:
                    path = Gtk.TreePath(line_number)
                    list_iterator = self.store.get_iter(path)
                    self.store.set_value(list_iterator, 1, 'No')

        def add_crawled(self, name_files):
            line_number = -1
            i = 0

            for filename in name_files:
                for row in self.store:
                    if row[0] == filename:
                        line_number = i
                    else:
                        i = i+1

                if line_number != -1:
                    path = Gtk.TreePath(line_number)
                    list_iterator = self.store.get_iter(path)
                    self.store.set_value(list_iterator, 1, 'Yes')

        def add_bold_font(self, name_files):
            line_number = -1
            i = 0

            for filename in name_files:
                for row in self.store:
                    if row[0] == filename:
                        line_number = i
                    else:
                        i = i+1

                if line_number != -1:
                    path = Gtk.TreePath(line_number)
                    list_iterator = self.store.get_iter(path)
                    self.store.set_value(list_iterator, 2, 700)

        def remove_bold_font(self, name_files):

            line_number = -1
            i = 0

            for filename in name_files:
                for row in self.store:
                    if row[0] == filename:
                        line_number = i
                    else:
                        i = i+1

                if line_number != -1:
                    path = Gtk.TreePath(line_number)
                    list_iterator = self.store.get_iter(path)
                    self.store.set_value(list_iterator, 2, 400)

    __instance = None

    def __init__(self, store, view):
        """ Virtually private constructor. """
        if TreeView.__instance is not None:
            raise Exception('This class is a singleton!')
        else:
            TreeView.__instance = TreeView.__TreeView(store, view)

    @staticmethod
    def get_instance():
        """ Static access method. """
        if TreeView.__instance is None:
            TreeView(None, None)
        return TreeView.__instance
