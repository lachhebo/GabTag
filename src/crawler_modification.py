from threading import Thread
from typing import Dict, List

from .dir_manager import DIR_MANAGER

from .crawler_data import DATA_CRAWLER
from .tools import is_selection_valid
from .treeview import TREE_VIEW
from .view import VIEW


class CrawlerModification(Thread):
    def __init__(self, modification: Dict, name_files: List):
        Thread.__init__(self)
        self.modification = modification
        self.file_names = name_files

    def run(self):

        names_file = DATA_CRAWLER.update_data_crawled(
            self.modification, DIR_MANAGER.directory
        )
        TREE_VIEW.manage_crawled(names_file)

        if is_selection_valid(self.file_names):
            data_scrapped = DATA_CRAWLER.get_tags(self.file_names)
            if is_selection_valid(self.file_names):
                if data_scrapped is not None:
                    VIEW.show_mbz(data_scrapped)
