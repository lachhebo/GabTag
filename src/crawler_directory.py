from threading import Thread
from .crawler_data import DATA_CRAWLER
from .model import MODEL


class CrawlerDirectory(Thread):
    def __init__(self, directory, store):
        Thread.__init__(self)
        self.data_crawler = DATA_CRAWLER
        self.directory = directory
        self.store = store
        self.model = MODEL

    def run(self):
        file_list = self.data_crawler.get_file_list(self.directory)

        file_list1 = file_list[0 : int(len(file_list) / 4)]
        file_list2 = file_list[int(len(file_list) / 4) : int(2 * len(file_list) / 4)]
        file_list3 = file_list[
            int(2 * len(file_list) / 4) : int(3 * len(file_list) / 4)
        ]
        file_list4 = file_list[int(3 * len(file_list) / 4) :]

        thread_pool = []
        file_list_pool = [file_list1, file_list2, file_list3, file_list4]

        for file_list_slice in file_list_pool:
            thread = Thread(
                target=self.data_crawler.get_data_from_online,
                args=(file_list_slice, self.directory),
            )
            thread.start()
            thread_pool.append(thread)

        for thread in thread_pool:
            thread.join()
