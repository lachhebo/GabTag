from abc import abstractmethod


class AudioExtensionHandler:
    @abstractmethod
    def get_tag(self, tag_key):
        pass

    @abstractmethod
    def set_tag(self, tag_key, tag_value):
        pass

    @abstractmethod
    def save_modifications(self):
        pass

    @abstractmethod
    def check_tag_existence(self, key):
        pass
