from typing import Dict, List

import musicbrainzngs as mb

# from .audio_getter import get_file_manager
from .tools import remove_extension, reorder_data
from .version import __version__


class DataCrawler:
    def __init__(self):
        mb.set_useragent(
            "GabTag", version=__version__, contact="ismael.lachheb@protonmail.com"
        )
        self.tag_founds = {}

    def crawl_one_file(self, name_file, directory):
        # audio = get_file_manager(name_file, directory)

        # tags = audio.get_tag_research()

        # if tags[0] == "" and tags[1] == "":
        self.search_by_filename(name_file)
        # elif tags[0] != "" and tags[1] != "":
        #    self.search_by_title_and_artist(name_file, tags)
        # elif tags[1] == "":
        #    self.search_by_title_and_album(name_file, tags)
        # elif tags[0] == "":
        #    self.search_by_artist_and_name_file(name_file, tags)

    def search_by_artist_and_name_file(self, name_file: str, tags: List):
        try:
            gathered_data = mb.search_recordings(
                query=remove_extension(name_file),
                artistname=tags[1],
                limit=1,
            )
            reordered_data = reorder_data(gathered_data)
            self.tag_founds[name_file] = reordered_data
        except mb.NetworkError:
            pass

    def search_by_title_and_album(self, name_file: str, tags):
        try:
            records = mb.search_recordings(recording=tags[0], release=tags[2], limit=1)
            records = reorder_data(records)
            self.tag_founds[name_file] = records
        except mb.NetworkError:
            pass

    def search_by_title_and_artist(self, name_file: str, tags):
        try:
            gathered_data = mb.search_recordings(
                recording=tags[0], artistname=tags[1], limit=1
            )
            self.tag_founds[name_file] = reorder_data(gathered_data)
        except mb.NetworkError:
            pass

    def search_by_filename(self, name_file: str):
        mz_query = remove_extension(name_file)
        self.tag_founds[name_file] = reorder_data(
            mb.search_recordings(query=mz_query, limit=1)
        )

    def update_data_crawled(self, modifications: Dict, directory: str) -> List:
        names_file = []
        for name_file in modifications:
            self.crawl_one_file(name_file, directory)
            names_file.append(name_file)
        return names_file

    def erase_data(self):
        self.tag_founds = {}

    def get_data_from_online(self, file_list, directory: str):
        for name_file in file_list:
            self.crawl_one_file(name_file, directory)

    def get_tags(self, names_files):

        tags_output = None

        name_file = names_files[0]
        if name_file in self.tag_founds:
            tags_output = self.tag_founds[name_file].copy()

        if len(names_files) > 1:
            for name_file in names_files:
                if name_file not in self.tag_founds:
                    return None
                _tags = ["artist", "album", "year", "genre", "cover"]
                for tag_iterator in _tags:
                    tag_test = self.tag_founds[name_file][tag_iterator]
                    if tags_output[tag_iterator] != tag_test:
                        tags_output[tag_iterator] = ""
                tags_output["title"] = ""
                tags_output["track"] = ""

        return tags_output


DATA_CRAWLER = DataCrawler()
