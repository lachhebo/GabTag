class SelectionHandler:
    def __init__(self):
        self.selection = None
        self.has_directory_change = False

    def update_dir(self):
        self.selection = None
        self.has_directory_change = True


SELECTION = SelectionHandler()
