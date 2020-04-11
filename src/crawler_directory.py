from threading import Thread
from .crawler_data import DataCrawler
from .model import Model


class CrawlerDirectory(Thread):

    def __init__(self, directory, store):
        Thread.__init__(self)
        self.data_crawler = DataCrawler.get_instance()
        self.directory = directory
        self.store = store
        self.model = Model.get_instance()

    def run(self):
        file_list = self.data_crawler.get_file_list(self.directory)

        file_list1 = []
        file_list2 = []
        file_list3 = []
        file_list4 = []

        i = 1
        for file in file_list:
            if i == 1:
                file_list1.append(file)
                i = 2
            elif i == 2:
                file_list2.append(file)
                i = 3
            elif i == 3:
                file_list3.append(file)
                i = 4
            elif i == 4:
                file_list4.append(file)
                i = 1

        thread_mbz1 = Thread(target=self.data_crawler.get_data_from_online,
                             args=(file_list1, self.directory))
        thread_mbz2 = Thread(target=self.data_crawler.get_data_from_online,
                             args=(file_list2, self.directory))
        thread_mbz3 = Thread(target=self.data_crawler.get_data_from_online,
                             args=(file_list3, self.directory))
        thread_mbz4 = Thread(target=self.data_crawler.get_data_from_online,
                             args=(file_list4, self.directory))

        thread_mbz1.start()
        thread_mbz2.start()
        thread_mbz3.start()
        thread_mbz4.start()

        thread_mbz1.join()
        thread_mbz2.join()
        thread_mbz3.join()
        thread_mbz4.join()
