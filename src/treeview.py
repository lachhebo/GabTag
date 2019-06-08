import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio, Gtk
from gi.repository import Pango
import logging

class TreeView:

    class __TreeView :

        def __init__(self,store, view):
            self.store = store
            self.view = view


            self.view.set_model(self.store)
            self.add_column("Name",0)
            self.add_column("Data Crawled",1)


        def remove_crawled(self,namefiles):
            finded = -1
            i = 0
            print("namesfiles :",namefiles)
            for filename in namefiles:
                for row in self.store :
                    if row[0] == filename :
                        print("found ",i)
                        finded = i
                    else :
                     i = i+1

                if finded != -1 :
                    print("set")
                    path = Gtk.TreePath(finded)
                    listiter = self.store.get_iter(path)
                    self.store.set_value(listiter,1,"No")


        def add_crawled(self,namefiles):
            finded = -1
            i = 0

            for filename in namefiles:
                for row in self.store :
                    if row[0] == filename :
                        print("found ",i)
                        finded = i
                    else :
                     i = i+1

                if finded != -1 :
                    print("set")
                    path = Gtk.TreePath(finded)
                    listiter = self.store.get_iter(path)
                    self.store.set_value(listiter,1,"Yes")


        def add_bold_font(self,namefile):
            """
            finded = -1
            i = 0

            for filename in namefiles:
                for row in self.store :
                    if row[0] == filename :
                        print("found ",i)
                        finded = i
                    else :
                     i = i+1

                if finded != -1 :
                    print("set")
                    path = Gtk.TreePath(finded)
                    listiter = self.store.get_iter(path)
                    self.store.set_value(listiter,1,Pango.Weight.BOLD)
            """
            pass

        def remove_bold_font(self,namefile):
            pass

        def add_column(self, namecolumn, text):
            '''
            A function to add a new column in the left panel treen useless in the code
            for the moment
            '''
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(namecolumn, renderer, text=text, weight_set=True)
            self.view.append_column(column)




    __instance = None

    def __init__(self,store,view):
        """ Virtually private constructor. """
        if TreeView.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            TreeView.__instance = TreeView.__TreeView(store,view)


    @staticmethod
    def getInstance():
        """ Static access method. """
        if TreeView.__instance == None:
            TreeView(None,None)
        return TreeView.__instance
