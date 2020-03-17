from threading import Thread
from .crawler_data import DataCrawler
from .model import Model
from .treeview import TreeView


class CrawlerModification(Thread):

    def __init__(self, modification, store, selection, some_file):
        Thread.__init__(self)
        self.data_crawler = DataCrawler.get_instance()
        self.model = Model.get_instance()
        self.directory = self.model.directory
        self.modification = modification
        self.store = store
        self.some_file = some_file
        self.selection = selection
        self.tree_view = TreeView.get_instance()

        model, list_iteration = self.model.selection.get_selected_rows()

        self.length_of_selection = len(list_iteration)
        self.file_names = []

        for i in range(len(list_iteration)):
            name_file = model[list_iteration[i]][0]
            self.file_names.append(name_file)

    def run(self):
        if self.some_file == 1:
            model, list_iteration = self.selection.get_selected_rows()

            for i in range(len(list_iteration)):  # TODO
                name_file = model[list_iteration[i]][0]
                if name_file in self.modification:
                    self.data_crawler.update_data_crawled(
                        [name_file], self.directory)

        else:
            self.data_crawler.update_data_crawled(self.modification, self.directory)

        if self.is_selection_equal_to(self.model.selection):
            model, list_iteration = self.model.selection.get_selected_rows()

            if len(list_iteration) > 1:
                multiple_line_selected = 1
            else:
                multiple_line_selected = 0

            data_scrapped = self.data_crawler.get_tags(
                model, list_iteration, multiple_line_selected)
            lyrics_scrapped = self.data_crawler.get_lyrics(
                model, list_iteration, multiple_line_selected)

            if self.is_selection_equal_to(self.model.selection):
                if data_scrapped is not None:
                    self.model.view.show_mbz(data_scrapped)
                if lyrics_scrapped is not None:  # TODO :Check why it happen to be None in some case :
                    self.model.view.show_lyrics(lyrics_scrapped)
        else:
            pass

    def is_selection_equal_to(self, selection):
        model, list_iteration = selection.get_selected_rows()

        if len(list_iteration) == self.length_of_selection:
            for i in range(len(list_iteration)):
                name_file = model[list_iteration[i]][0]
                if name_file not in self.file_names:
                    return False
        else:
            return False

        return True
