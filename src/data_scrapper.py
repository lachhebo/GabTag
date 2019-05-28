import musicbrainzngs as mb



class Data_Scrapper :

    def __init__(self):
        mb.set_useragent("GabTag", version = "1.0.5", contact = "ismael.lachheb@protonmail.com")



    def getTags(self,model,listiter, tagdico):

        namefile = model[listiter][0]

        #print(mb.search_releases(artist=tagdico["artist"]["value"],limit=5))
    
