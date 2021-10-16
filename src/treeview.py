from typing import List

import gi
from gi.repository import Gtk

gi.require_version("Gtk", "3.0")


class TreeView:
    def __init__(self, store, view):
        self.store = store
        self.view = view

    def add_columns(self):
        if self.store is not None and self.view is not None:
            self.view.set_model(self.store)

            renderer_filename = Gtk.CellRendererText()
            column_filename = Gtk.TreeViewColumn(
                "filename", renderer_filename, text=0, weight=2, weight_set=True
            )

            renderer_data = Gtk.CellRendererText()
            column_data_gathered = Gtk.TreeViewColumn(
                "data gathered", renderer_data, text=1, weight=2, weight_set=True
            )

            self.view.append_column(column_data_gathered)
            self.view.append_column(column_filename)

    def update_tree_view_list(self, file_names: List):
        """
        Erase the list in the tree view and then update it with filename
        with extension handled by GabTag
        """

        self.store.clear()

        for name_file in file_names:
            self.store.append([name_file, "No", 400])

    def manage_crawled(self, name_files, add=True):
        line_number = -1
        i = 0

        for filename in name_files:
            for row in self.store:
                if row[0] == filename:
                    line_number = i
                else:
                    i = i + 1

            if line_number != -1:
                path = Gtk.TreePath(line_number)
                list_iterator = self.store.get_iter(path)
                if add:
                    self.store.set_value(list_iterator, 1, "Yes")
                else:
                    self.store.set_value(list_iterator, 1, "No")

    def manage_bold_font(self, name_files, add=True):
        line_number = -1
        i = 0

        for filename in name_files:
            for row in self.store:
                if row[0] == filename:
                    line_number = i
                else:
                    i = i + 1

            if line_number != -1:
                path = Gtk.TreePath(line_number)
                list_iterator = self.store.get_iter(path)
                if add:
                    self.store.set_value(list_iterator, 2, 700)
                else:
                    self.store.set_value(list_iterator, 2, 400)


TREE_VIEW = TreeView(None, None)
