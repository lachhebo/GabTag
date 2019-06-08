from threading import Thread, RLock
from .data_crawler import Data_Crawler
from .model import Model
import time

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

            filelist = self.data_crawler.get_filelist(self.directory)

            filelist1 = []
            filelist2 = []
            filelist3 = []
            filelist4 = []

            i= 1
            for filen in filelist :
                if i == 1:
                    filelist1.append(filen)
                    i = 2
                elif i == 2:
                    filelist2.append(filen)
                    i = 3
                elif i == 3 :
                    filelist3.append(filen)
                    i = 4
                elif i == 4 :
                    filelist4.append(filen)
                    i = 1

            thread_mbz1 = Thread(target = self.data_crawler.get_data_from_online, args=(filelist1,self.directory)) #Writing data
            thread_mbz2 = Thread(target = self.data_crawler.get_data_from_online, args=(filelist2,self.directory))
            thread_mbz3 = Thread(target = self.data_crawler.get_data_from_online, args=(filelist3,self.directory))
            thread_mbz4 = Thread(target = self.data_crawler.get_data_from_online, args=(filelist4,self.directory))


            thread_mbz1.start()
            thread_mbz2.start()
            thread_mbz3.start()
            thread_mbz4.start()

            '''
            while not self.data_crawler.is_finished(filelist):
                time.sleep(0.3)
                selection = self.model.selection
                if selection != None :
                    model, listiter = selection.get_selected_rows()
                    print("model", len(listiter))
                    if len(listiter) == 1:
                        if model[listiter][0] in self.data_crawler.tag_finder and model[listiter][0] in self.data_crawler.lyrics:

                            data_scrapped = self.data_crawler.get_tags(model, listiter, 0)
                            lyrics_scrapped = self.data_crawler.get_lyrics(model, listiter, 0)

                            print("data scrapped", data_scrapped)

                            self.model.view.show_mbz(data_scrapped)
                            self.model.view.show_lyrics(lyrics_scrapped)


            '''

            thread_mbz1.join()
            thread_mbz2.join()
            thread_mbz3.join()
            thread_mbz4.join()



