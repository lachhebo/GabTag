from src.crawler_data import DataCrawler
from unittest.mock import Mock, patch

TESTED_MODULE = "src.crawler_data"


@patch(f"{TESTED_MODULE}.DataCrawler.search_by_filename")
@patch(f"{TESTED_MODULE}.get_file_manager")
def test_crawl_one_file__when_crawling_we_start_by_searching_by_filename_if_no_title_nor_artist(
    mock_file, mock_search
):
    # given
    data_crawler = DataCrawler()
    audio = Mock()
    audio.get_tag_research.return_value = ["", "", ""]
    mock_file.return_value = audio

    # when
    data_crawler.crawl_one_file("fake_filename", "fake_dir")

    # then
    mock_search.assert_called_with("fake_filename")


@patch(f"{TESTED_MODULE}.DataCrawler.search_by_title_and_artist")
@patch(f"{TESTED_MODULE}.get_file_manager")
def test_crawl_one_file__when_crawling_we_start_by_searching_by_title_and_artist_if_there_available(
    mock_file, mock_search
):
    # given
    data_crawler = DataCrawler()
    audio = Mock()
    audio.get_tag_research.return_value = ["title", "artist", "", "", ""]
    mock_file.return_value = audio

    # when
    data_crawler.crawl_one_file("fake_filename", "fake_dir")

    # then
    mock_search.assert_called_with("fake_filename", ["title", "artist", "", "", ""])


@patch(f"{TESTED_MODULE}.DataCrawler.search_by_artist_and_name_file")
@patch(f"{TESTED_MODULE}.get_file_manager")
def test_crawl_one_file__when_crawling_we_start_by_searching_by_artist_and_filename_if_no_artist(
    mock_file, mock_search
):
    # given
    data_crawler = DataCrawler()
    audio = Mock()
    audio.get_tag_research.return_value = ["", "artist", "album", "", ""]
    mock_file.return_value = audio

    # when
    data_crawler.crawl_one_file("fake_filename", "fake_dir")

    # then
    mock_search.assert_called_with("fake_filename", ["", "artist", "album", "", ""])


def test_get_tags__smash_title_and_track_name_for_multiple_values():
    # given
    crawler = DataCrawler()
    gmodel = {"file1": ["fake_file.mp3"], "file2": ["fake_second_file.mp3"]}
    list_iterator = ["file1", "file2"]
    crawler.tag_founds = {
        "fake_file.mp3": {
            "title": " ftitle",
            "artist": "fartist",
            "genre": "fgenre",
            "year": "fyear",
            "album": "falbum",
            "cover": "fcover",
            "track": "33",
        },
        "fake_second_file.mp3": {
            "title": " ftitle",
            "artist": "fartist",
            "genre": "fgenre",
            "year": "fyear2",
            "album": "falbum2",
            "cover": "fcover2",
            "track": "33",
        },
    }

    # when
    output = crawler.get_tags(gmodel, list_iterator)

    # then
    assert output == {
        "title": "",
        "artist": "fartist",
        "genre": "fgenre",
        "year": "",
        "album": "",
        "cover": "",
        "track": "",
    }
