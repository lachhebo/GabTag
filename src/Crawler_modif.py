from threading import Thread, RLock
from .data_crawler import Data_Crawler
from .model import Model

verrou = RLock()

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


        model, listiter = self.model.selection.get_selected_rows()

        self.lenselection = len(listiter)
        self.filenames = []

        for i in range(len(listiter)):
                namefile = model[listiter[i]][0]
                self.filenames.append(namefile)

        '''

        model, listiter = selection.get_selected_rows()

            for i in range(len(listiter)): ## TODO
                namefile = model[listiter[i]][0]
                audio = self.moteur.getFile(namefile, self.directory)
                if namefile in self.modification :
                    filemodifs = self.modification[namefile]

        thread_mbz = threading.Thread(target = self.data_crawler.update_data_crawled, args=([namefile],self.directory)) #Writing data
        thread_mbz.start()
        '''


        '''
        thread_mbz = threading.Thread(target = self.data_crawler.update_data_crawled, args=(self.modification.copy(),self.directory)) #Writing data
        thread_mbz.start()
        '''


    def run(self):
            """Code à exécuter pendant l'exécution du thread."""
            if self.some_file == 1 :
                print("modified some tags :")
                model, listiter = self.selection.get_selected_rows()

                for i in range(len(listiter)): ## TODO
                    namefile = model[listiter[i]][0]
                    if namefile in self.modifs :
                        self.data_crawler.update_data_crawled([namefile],self.directory)

            else :
                self.data_crawler.update_data_crawled(self.modifs,self.directory)

            print("model selection :", self.model.selection)


            if(self.selectionequal(self.model.selection)):
                print("deltaducongo")
                model, listiter = self.model.selection.get_selected_rows()

                if len(listiter)> 1 :
                    multiple_line_selected = 1
                else :
                    multiple_line_selected = 0


                data_scrapped = self.data_crawler.get_tags(model, listiter, multiple_line_selected)
                lyrics_scrapped = self.data_crawler.get_lyrics(model, listiter, multiple_line_selected)

                self.model.view.show_mbz(data_scrapped)
                self.model.view.show_lyrics(lyrics_scrapped)
            else :
                print("lecaire")



    def selectionequal(self,selec):
        model, listiter = selec.get_selected_rows()
        print("la taille est :", len(listiter) )
        print("la taille autorisée :",self.lenselection )
        ala = len(listiter)
        bab =  self.lenselection

        if ala == bab :
            for i in range(len(listiter)):
                namefile = model[listiter[i]][0]
                if namefile not in self.filenames:
                    print("why element ? ",namefile)
                    return False
        else :
            print("why size ?")
            return False

        return True

        
