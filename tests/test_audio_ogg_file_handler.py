from unittest.mock import patch, Mock, call

from src.audio_ogg_file_handler import OggFileHandler

TESTED_MODULE = "src.audio_ogg_file_handler"


def test_get_extension__return_ogg():
    # given

    # when
    result = OggFileHandler.get_extension()

    # then
    assert result == ".ogg"


@patch(f"{TESTED_MODULE}.OGG")
def test_get_one_tag__return_empty_string_if_no_id3(m_ogg):
    # given
    oggfilehandler = OggFileHandler("fake_path.ogg")
    oggfilehandler.id3 = Mock()
    oggfilehandler.id3.get.return_value = []

    # when
    result = oggfilehandler.get_one_tag("title", "text")

    # then
    assert result == ""


@patch(f"{TESTED_MODULE}.MP3")
def test_get_one_tag__return_tag_if_id3_with_text(m_ogg):
    # given
    oggfilehandler = OggFileHandler("fake_path.ogg")
    oggfilehandler.id3 = Mock()
    fake_tag = Mock()
    fake_tag.text = ["title"]
    oggfilehandler.id3.get.return_value = [fake_tag]

    # when
    result = oggfilehandler.get_one_tag("title", "text")

    # then
    assert result == "title"


@patch(f"{TESTED_MODULE}.MP3")
def test_get_one_tag__return_tag_if_id3_with_data(m_ogg):
    # given
    oggfilehandler = OggFileHandler("fake_path.ogg")
    oggfilehandler.id3 = Mock()
    fake_tag = Mock()
    fake_tag.data = ["data"]
    oggfilehandler.id3.get.return_value = [fake_tag]

    # when
    result = oggfilehandler.get_one_tag("title", "data")

    # then
    assert result == ["data"]


@patch(f"{TESTED_MODULE}.MP3")
@patch(f"{TESTED_MODULE}.OgFileHandler.get_one_tag")
def test_get_tag_research__return_title_artist_and_album(m_get, m_ogg):
    # given
    oggfilehandler = OggFileHandler("fake_path.ogg")
    oggfilehandler.id3 = Mock()
    calls = [call("TITLE", "text"), call("ARTIST", "text"), call("ALBUM", "text")]

    # when
    oggfilehandler.get_tag_research()

    # then
    m_get.assert_has_calls(calls=calls, any_order=True)
