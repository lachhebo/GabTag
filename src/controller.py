from threading import Thread
from typing import List

from .crawler_data import DATA_CRAWLER
from .crawler_directory import CrawlerDirectory
from .crawler_modification import CrawlerModification
from .dir_manager import DIR_MANAGER
from .model import MODEL
from .selection_handler import SELECTION
from .treeview import TREE_VIEW
from .tools import get_file_list, is_selection_valid, get_filenames_from_selection

import gi

from .view import VIEW

gi.require_version("Gtk", "4.0")


class Controller:
    @staticmethod
    def wait_for_mbz(names_files):
        is_waiting_mbz = True
        while is_selection_valid(names_files) and is_waiting_mbz:
            data_gat = DATA_CRAWLER.get_tags(names_files)
            if data_gat is not None and is_selection_valid(names_files):
                VIEW.show_mbz(data_gat)
                is_waiting_mbz = False

    @staticmethod
    def update_directory(directory: str):
        SELECTION.update_dir()
        DIR_MANAGER.directory = directory
        DIR_MANAGER.file_names = get_file_list(directory)
        DIR_MANAGER.is_open_directory = True
        TREE_VIEW.update_tree_view_list(DIR_MANAGER.file_names)
        MODEL.reset_all()

    @staticmethod
    def reset_all():  # TODO: check it
        """
        Cancel modification before it being saved
        and update the view,it supposes that something
        is selection (True)
        """
        VIEW.erase()
        MODEL.reset_all()
        # VIEW.update_view()
        # TREE_VIEW.manage_bold_font(names_file, add=False)

    @staticmethod
    def reset_one(name_files: List):
        """
        Find the selected rows and delete the related dictionary
        nested in modifications. Then update view
        """
        MODEL.reset(name_files)
        TREE_VIEW.manage_bold_font(name_files, add=False)

    @staticmethod
    def crawl_thread_modification():
        thread = CrawlerModification(MODEL.modification.copy(), TREE_VIEW.store)
        MODEL.save_modifications(TREE_VIEW, directory=DIR_MANAGER.directory)
        thread.start()

    @staticmethod
    def save_some_files():
        name_files = get_filenames_from_selection(SELECTION.selection)
        thread = CrawlerModification(MODEL.modification.copy(), name_files)
        # print("save for some file")
        MODEL.save_modifications(TREE_VIEW, name_files=name_files, directory=DIR_MANAGER.directory)
        thread.start()
        VIEW.erase()
        MODEL.erase_tag()

        try:
            multiple_line_selected = MODEL.set_tags_dictionary(name_files, DIR_MANAGER.directory)  # return a int
            data_scrapped = DATA_CRAWLER.get_tags(name_files)
            # print("model", MODEL.tags_dictionary)
            # print("multiples", multiple_line_selected)
            VIEW.show_tags(MODEL.tags_dictionary, multiple_line_selected)
        except Exception as e:
            # print("issue with bug", e)
            VIEW.show_mbz(
                {
                    "title": "",
                    "artist": "",
                    "album": "",
                    "track": "",
                    "year": "",
                    "genre": "",
                    "cover": "",
                }
            )

            VIEW.show_tags(
                {
                "title": "",
                "album": "",
                "artist": "",
                "genre": "",
                "cover": "",
                "year": "",
                "track": "",
                "length": "",
                "size": "",
            },
            1
            )
            return
        
        if data_scrapped is None:
            VIEW.show_mbz(
                {
                    "title": "",
                    "artist": "",
                    "album": "",
                    "track": "",
                    "year": "",
                    "genre": "",
                    "cover": "",
                }
            )

            thread_waiting_mbz = Thread(
                target=Controller.wait_for_mbz,
                args=(name_files,),
            )
            thread_waiting_mbz.start()
        else:
            VIEW.show_mbz(data_scrapped)


    @staticmethod
    def reset_some_files():
        name_files = get_filenames_from_selection(SELECTION.selection)
        Controller.reset_one(name_files)

    @staticmethod
    def change_directory(directory):
        VIEW.erase()
        SELECTION.update_dir()
        Controller.update_directory(directory)
        thread = CrawlerDirectory(directory)
        thread.start()

    @staticmethod
    def react_to_user_modif(tag: str, text: str):
        name_files = get_filenames_from_selection(SELECTION.selection)
        MODEL.update_modifications(name_files, tag, text, DIR_MANAGER.directory)
        TREE_VIEW.manage_bold_font(name_files)

    @staticmethod
    def update_view(names_files: List):
        """
        Erase the view and the current tag value then get tags for
        selected row (or rows) and show them.
        """
        VIEW.erase()
        MODEL.erase_tag()


        try:
            multiple_line_selected = MODEL.set_tags_dictionary(names_files, DIR_MANAGER.directory)  # return a int
            data_scrapped = DATA_CRAWLER.get_tags(names_files)
            VIEW.show_tags(MODEL.tags_dictionary, multiple_line_selected)
        except Exception as e:
            # print("issue with bug", e)
            VIEW.show_mbz(
                {
                    "title": "",
                    "artist": "",
                    "album": "",
                    "track": "",
                    "year": "",
                    "genre": "",
                    "cover": "",
                }
            )

            VIEW.show_tags(
                {
                "title": "",
                "album": "",
                "artist": "",
                "genre": "",
                "cover": "",
                "year": "",
                "track": "",
                "length": "",
                "size": "",
            },
            1
            )
            return



        if data_scrapped is None:
            VIEW.show_mbz(
                {
                    "title": "",
                    "artist": "",
                    "album": "",
                    "track": "",
                    "year": "",
                    "genre": "",
                    "cover": "",
                }
            )

            thread_waiting_mbz = Thread(
                target=Controller.wait_for_mbz,
                args=(names_files,),
            )
            thread_waiting_mbz.start()
        else:
            VIEW.show_mbz(data_scrapped)
