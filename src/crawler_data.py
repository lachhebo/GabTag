from os import walk

import musicbrainzngs as mb
from PyLyrics import *

from .audio_getter import is_extension_managed, get_file_manager
from .tools import remove_extension, reorder_data
from .treeview import TreeView
from .view import View


class DataCrawler:
    class __DataCrawler:

        def __init__(self):
            try:
                mb.set_useragent('GabTag', version='1.3.4',
                                 contact='ismael.lachheb@protonmail.com')
                self.internet = True
            except:
                self.internet = False
            self.tag_finder = {}
            self.lyrics = {}
            self.view = View.get_instance()
            self.tree_view = TreeView.get_instance()
            self.directory = ''

        def crawl_one_file(self, name_file, directory):
            if is_extension_managed(name_file) and self.internet == True:
                audio = get_file_manager(name_file, directory)

                tags = audio.get_tag_research()

                if tags[0] == '' and tags[1] == '':
                    # Either filename if no_tags
                    mz_query = remove_extension(name_file)
                    self.tag_finder[name_file] = reorder_data(
                        mb.search_recordings(query=mz_query, limit=1))
                    self.tree_view.add_crawled([name_file])
                else:
                    # Using tags title artist and album if they are present
                    if tags[0] != '' and tags[1] != 0:
                        try:
                            gathered_data = mb.search_recordings(recording=tags[0], artistname=tags[1], limit=1)
                            self.tag_finder[name_file] = reorder_data(gathered_data)
                            self.tree_view.add_crawled([name_file])
                        except:  # TODO Check Internet Connection
                            pass

                    elif tags[1] == '':
                        try:
                            self.tag_finder[name_file] = reorder_data(
                                mb.search_recordings(recording=tags[0], release=tags[2], limit=1))
                            self.tree_view.add_crawled([name_file])
                        except:
                            pass

                    elif tags[0] == '':
                        try:
                            self.tag_finder[name_file] = reorder_data(mb.search_recordings(
                                query=remove_extension(name_file), artistname=tags[1], limit=1))
                            self.tree_view.add_crawled([name_file])
                        except:
                            self.tree_view.add_crawled([name_file])

                    else:
                        self.tree_view.add_crawled([name_file])

        def crawl_lyrics(self, name_file, directory):
            if is_extension_managed(name_file) and self.internet == True:
                audio = get_file_manager(name_file, directory)

                tags = audio.get_tag_research()

                if tags[0] == '' or tags[1] == '':
                    pass
                else:
                    try:
                        self.lyrics[name_file] = PyLyrics.getLyrics(
                            tags[1], tags[0])
                    except:
                        self.lyrics[name_file] = ''

        def update_data_crawled(self, modifications, directory):
            for name_file in modifications:
                self.tree_view.remove_crawled([name_file])
                if self.stop(directory):
                    break
                self.crawl_one_file(name_file, directory)
                if self.stop(directory):
                    break
                self.crawl_lyrics(name_file, directory)

        def erase_data(self):
            self.tag_finder = {}
            self.lyrics = {}

        def get_file_list(self, directory):
            self.directory = directory

            file_list = []
            for (_, _, file_names) in walk(directory):
                file_list.extend(file_names)
                break

            return file_list

        def get_data_from_online(self, file_list, directory):

            for name_file in file_list:
                if is_extension_managed(name_file) and self.internet == True:

                    if self.stop(directory):
                        break

                    self.crawl_one_file(name_file, directory)
                    self.crawl_lyrics(name_file, directory)

                    if self.stop(directory):
                        break

        def is_finished(self, file_list):
            for name_file in file_list:
                if name_file in self.tag_finder:
                    if name_file not in self.lyrics:
                        return False
                else:
                    return False
            return True

        def stop(self, directory):
            if self.directory == directory:
                return False
            else:
                return True

        def update_directory(self, directory):
            self.directory = directory

        def get_lyrics(self, model, list_iterator, is_multiples_line_selected):
            if is_multiples_line_selected:
                return 'No lyrics on Multiple File'
            else:
                name_file = model[list_iterator][0]
                if name_file in self.lyrics:
                    if self.lyrics[name_file] != '':
                        return self.lyrics[name_file]
                    else:
                        return 'Lyrics not available'
                else:
                    return None

        def get_tags(self, model, list_iterator, is_multiple_lines_selected):

            if is_multiple_lines_selected == 0:

                name_file = model[list_iterator][0]
                if name_file in self.tag_finder:
                    return self.tag_finder[name_file].copy()
                else:
                    return None

            elif is_multiple_lines_selected == 1:

                name_file = model[list_iterator][0]
                if name_file in self.tag_finder:
                    candidat = self.tag_finder[name_file].copy()
                else:
                    return None

                for i in range(1, len(list_iterator)):
                    beta = model[list_iterator[i]][0]
                    if beta in self.tag_finder:
                        for tag_iterator in ['artist', 'album', 'year', 'genre', 'cover']:
                            if candidat[tag_iterator] != self.tag_finder[beta][tag_iterator]:
                                candidat[tag_iterator] = ''
                        candidat['title'] = ''
                        candidat['track'] = ''
                    else:
                        return None

                return candidat

    __instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if DataCrawler.__instance is not None:
            raise Exception('This class is a singleton!')
        else:
            DataCrawler.__instance = DataCrawler.__DataCrawler()

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DataCrawler.__instance is None:
            DataCrawler()
        return DataCrawler.__instance
