from threading import Thread
from .data_crawler import Data_Crawler
from .model import Model
from .treeview import TreeView


class Crawler_Modif(Thread):

    def __init__(self, modifs, store, selection, some_file):
        Thread.__init__(self)

        self.data_crawler = Data_Crawler.getInstance()
        self.model = Model.getInstance()
        self.directory = self.model.directory
        self.modifs = modifs
        self.store = store
        self.some_file = some_file
        self.selection = selection
        self.treeview = TreeView.getInstance()

        model, listiter = self.model.selection.get_selected_rows()

        self.lenselection = len(listiter)
        self.filenames = []

        for i in range(len(listiter)):
            namefile = model[listiter[i]][0]
            self.filenames.append(namefile)

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        if self.some_file == 1:
            model, listiter = self.selection.get_selected_rows()

            for i in range(len(listiter)):  # TODO
                namefile = self.model.title2filename(model[listiter[i]][0]) 
                if namefile in self.modifs:
                    self.data_crawler.update_data_crawled(
                        [namefile], self.directory)

        else:
            self.data_crawler.update_data_crawled(self.modifs, self.directory)

        if(self.selectionequal(self.model.selection)):
            model, listiter = self.model.selection.get_selected_rows()

            if len(listiter) > 1:
                multiple_line_selected = 1
            else:
                multiple_line_selected = 0

            data_scrapped = self.data_crawler.get_tags(
                model, listiter, multiple_line_selected, self.model.filenames)
            lyrics_scrapped = self.data_crawler.get_lyrics(
                model, listiter, multiple_line_selected, self.model.filenames)

            if(self.selectionequal(self.model.selection)):
                if data_scrapped != None:
                    self.model.view.show_mbz(data_scrapped)
                if lyrics_scrapped != None:  # TODO :Check why it happend to be None in some case :
                    self.model.view.show_lyrics(lyrics_scrapped)
        else:
            pass

    def selectionequal(self, selec):
        model, listiter = selec.get_selected_rows()

        if len(listiter) == self.lenselection:
            for i in range(len(listiter)):
                namefile = model[listiter[i]][0]
                if namefile not in self.filenames:
                    return False
        else:
            return False

        return True
