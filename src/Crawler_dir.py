from threading import Thread
from .data_crawler import Data_Crawler
from .model import Model
import time


class Crawler_Dir(Thread):

    def __init__(self, directory, store):
        Thread.__init__(self)
        self.data_crawler = Data_Crawler.getInstance()
        self.directory = directory
        self.store = store
        self.model = Model.getInstance()

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        filelist = self.model.filenames

        filelist1 = []
        filelist2 = []
        filelist3 = []
        filelist4 = []

        i = 1
        for filetuple in filelist:
            if i == 1:
                filelist1.append(filetuple[0])
                i = 2
            elif i == 2:
                filelist2.append(filetuple[0])
                i = 3
            elif i == 3:
                filelist3.append(filetuple[0])
                i = 4
            elif i == 4:
                filelist4.append(filetuple[0])
                i = 1

        thread_mbz1 = Thread(target=self.data_crawler.get_data_from_online, args=(
            filelist1, self.directory))  # Writing data
        thread_mbz2 = Thread(target=self.data_crawler.get_data_from_online, args=(
            filelist2, self.directory))
        thread_mbz3 = Thread(target=self.data_crawler.get_data_from_online, args=(
            filelist3, self.directory))
        thread_mbz4 = Thread(target=self.data_crawler.get_data_from_online, args=(
            filelist4, self.directory))

        thread_mbz1.start()
        thread_mbz2.start()
        thread_mbz3.start()
        thread_mbz4.start()

        thread_mbz1.join()
        thread_mbz2.join()
        thread_mbz3.join()
        thread_mbz4.join()
