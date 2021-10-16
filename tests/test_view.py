from unittest.mock import Mock

from src.view import View


def test__erase__set_text_to_empty_string_for_each_entry():
    # given
    test_view = View()
    test_view.title = Mock()
    test_view.album = Mock()
    test_view.artist = Mock()
    test_view.genre = Mock()
    test_view.track = Mock()
    test_view.year = Mock()
    test_view.show_mbz = Mock()
    test_view.cover = Mock()

    # when
    test_view.erase()

    # then
    test_view.title.set_text.assert_called_with("")
    test_view.album.set_text.assert_called_with("")
    test_view.artist.set_text.assert_called_with("")
    test_view.genre.set_text.assert_called_with("")
    test_view.track.set_text.assert_called_with("")
    test_view.year.set_text.assert_called_with("")
    test_view.cover.set_from_icon_name.assert_called()
    test_view.show_mbz.assert_called_with(
        {
            "title": "",
            "track": "",
            "album": "",
            "genre": "",
            "artist": "",
            "cover": "",
            "year": "",
        }
    )


def test_show_tags__apply_all_tags_correctly():
    # given
    test_view = View()
    test_view.title = Mock()
    test_view.album = Mock()
    test_view.artist = Mock()
    test_view.genre = Mock()
    test_view.track = Mock()
    test_view.year = Mock()
    test_view.show_mbz = Mock()

    test_view.length = Mock()
    test_view.size = Mock()

    test_view.cover = Mock()
    tags_dict = {
        "title": "fake_title",
        "track": "1",
        "album": "fake_album",
        "artist": "fake_artist",
        "length": "fake_length",
        "cover": "",
        "genre": "fake_genre",
        "size": "33",
        "year": "2021",
    }

    # when
    test_view.show_tags(tags_dict, 0)

    # then
    test_view.length.set_text.assert_called_with("fake_length")
    test_view.size.set_text.assert_called_with("33")

    test_view.genre.set_text.assert_called_with("fake_genre")
    test_view.album.set_text.assert_called_with("fake_album")
    test_view.artist.set_text.assert_called_with("fake_artist")
    test_view.year.set_text.assert_called_with("2021")

    test_view.title.set_text.assert_called_with("fake_title")
    test_view.title.set_editable.assert_called_with(1)

    test_view.track.set_text.assert_called_with("1")
    test_view.track.set_editable.assert_called_with(1)


def test_show_tags__apply_all_tags_correctly_if_multiple_tag():
    # given
    test_view = View()
    test_view.title = Mock()
    test_view.album = Mock()
    test_view.artist = Mock()
    test_view.genre = Mock()
    test_view.track = Mock()
    test_view.year = Mock()
    test_view.show_mbz = Mock()

    test_view.length = Mock()
    test_view.size = Mock()

    test_view.cover = Mock()
    tags_dict = {
        "title": "fake_title",
        "track": "1",
        "album": "fake_album",
        "artist": "fake_artist",
        "length": "fake_length",
        "cover": "",
        "genre": "fake_genre",
        "size": "33",
        "year": "2021",
    }

    # when
    test_view.show_tags(tags_dict, 1)

    # then
    test_view.length.set_text.assert_called_with("")
    test_view.size.set_text.assert_called_with("")

    test_view.genre.set_text.assert_called_with("fake_genre")
    test_view.album.set_text.assert_called_with("fake_album")
    test_view.artist.set_text.assert_called_with("fake_artist")
    test_view.year.set_text.assert_called_with("2021")

    test_view.title.set_text.assert_called_with("")
    test_view.title.set_editable.assert_called_with(0)

    test_view.track.set_text.assert_called_with("")
    test_view.track.set_editable.assert_called_with(0)
