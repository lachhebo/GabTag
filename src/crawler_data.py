import musicbrainzngs as mb
import requests
from os import walk
from PyLyrics import getLyrics
from .audio_getter import is_extension_managed, get_file_manager
from .tools import remove_extension, reorder_data
from .treeview import TreeView
from .version import __version__
from .view import View


class DataCrawler:
    class __DataCrawler:

        def __init__(self):
            mb.set_useragent(
                'GabTag',
                version=__version__,
                contact='ismael.lachheb@protonmail.com')
            self.tag_finder = {}
            self.lyrics = {}
            self.view = View.get_instance()
            self.tree_view = TreeView.get_instance()
            self.directory = ''

        def crawl_one_file(self, name_file, directory):
            if is_extension_managed(name_file):
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
                            gathered_data = mb.search_recordings(
                                recording=tags[0], artistname=tags[1], limit=1)
                            self.tag_finder[name_file] = reorder_data(
                                gathered_data)
                            self.tree_view.add_crawled([name_file])
                        except mb.NetworkError:
                            pass

                    elif tags[1] == '':
                        try:
                            records = mb.search_recordings(recording=tags[0],
                                                           release=tags[2],
                                                           limit=1)
                            records = reorder_data(records)
                            self.tag_finder[name_file] = records
                            self.tree_view.add_crawled([name_file])
                        except mb.NetworkError:
                            pass

                    elif tags[0] == '':
                        try:
                            gathered_data = mb.search_recordings(
                                query=remove_extension(name_file),
                                artistname=tags[1],
                                limit=1)
                            reordered_data = reorder_data(gathered_data)
                            self.tag_finder[name_file] = reordered_data
                            self.tree_view.add_crawled([name_file])
                        except mb.NetworkError:
                            self.tree_view.add_crawled([name_file])

                    else:
                        self.tree_view.add_crawled([name_file])

        def crawl_lyrics(self, name_file, directory):
            if is_extension_managed(name_file):
                audio = get_file_manager(name_file, directory)

                tags = audio.get_tag_research()

                if tags[0] == '' or tags[1] == '':
                    pass
                else:
                    try:
                        self.lyrics[name_file] = getLyrics(
                            tags[1], tags[0])
                    except requests.exceptions.ConnectionError:
                        self.lyrics[name_file] = ''
                    except ValueError:
                        messge = 'Lyrics not available for this song or artist'
                        self.lyrics[name_file] = messge

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
                if is_extension_managed(name_file):

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
                        _tags = ['artist', 'album', 'year', 'genre', 'cover']
                        for tag_iterator in _tags:
                            tag_test = self.tag_finder[beta][tag_iterator]
                            if candidat[tag_iterator] != tag_test:
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
