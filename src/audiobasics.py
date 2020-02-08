import abc


class AudioBasics():

    @abc.abstractmethod
    def getTag(self, tag_key):
        pass

    @abc.abstractmethod
    def setTag(self, tag_key, tag_value):
        pass

    @abc.abstractmethod
    def savemodif(self):
        pass

    @abc.abstractmethod
    def check_tag_existence(self, key):
        pass
