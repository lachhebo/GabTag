from threading import Thread

from .crawler_data import DATA_CRAWLER
from .dir_manager import DIR_MANAGER
from .tools import get_file_list
from .treeview import TREE_VIEW


def split(file_list, n=1):
    k, m = divmod(len(file_list), n)
    return (
        file_list[i * k + min(i, m): (i + 1) * k + min(i + 1, m)] for i in range(n)
    )


class CrawlerDirectory(Thread):
    def __init__(self, directory):
        Thread.__init__(self)
        self.directory = directory

    def run(self):
        file_list = get_file_list(self.directory)
        file_list_pool = split(file_list)

        thread_pool = []
        for file_list_slice in file_list_pool:
            thread = Thread(
                target=DATA_CRAWLER.get_data_from_online,
                args=(file_list_slice,DIR_MANAGER.directory),
            )
            thread.start()
            thread_pool.append(thread)

        marked = []
        while True in [thread.is_alive() for thread in thread_pool]:
            self.check_and_mark_file_crawled(marked)

        self.check_and_mark_file_crawled(marked)

    def check_and_mark_file_crawled(self, marked):
        for file_name in DATA_CRAWLER.tag_founds.copy().keys():
            if file_name not in marked and self.directory == DIR_MANAGER.directory:
                TREE_VIEW.manage_crawled([file_name])
                marked.append(file_name)
