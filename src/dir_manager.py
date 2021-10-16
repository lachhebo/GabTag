from typing import List


class DirectoryManager:
    def __init__(self):
        self.directory: str = ""
        self.file_names: List = []
        self.is_open_directory = False

    def clear(self):
        self.directory = ""
        self.file_names = []
        self.is_open_directory = False


DIR_MANAGER = DirectoryManager()
