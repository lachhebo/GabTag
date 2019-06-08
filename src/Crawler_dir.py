from threading import Thread, RLock
from .data_crawler import Data_Crawler
from .model import Model

verrou = RLock()

class Crawler_Dir(Thread):

    def __init__(self, directory, store):
        Thread.__init__(self)
        self.data_crawler = Data_Crawler.getInstance()
        self.directory = directory
        self.store = store
        self.model = Model.getInstance()


    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        with verrou :
            self.data_crawler.crawl_data(self.directory,self.store)


