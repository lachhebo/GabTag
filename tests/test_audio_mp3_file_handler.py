from unittest.mock import patch, Mock, call

from src.audio_mp3_file_handler import Mp3FileHandler

TESTED_MODULE = "src.audio_mp3_file_handler"


def test_get_extension__return_mp3():
    # given

    # when
    result = Mp3FileHandler.get_extension()

    # then
    assert result == ".mp3"


@patch(f"{TESTED_MODULE}.MP3")
def test_get_one_tag__return_empty_string_if_no_id3(m_mp3):
    # given
    mp3filehandler = Mp3FileHandler("fake_path.mp3")
    mp3filehandler.id3 = Mock()
    mp3filehandler.id3.getall.return_value = []

    # when
    result = mp3filehandler.get_one_tag("title", "text")

    # then
    assert result == ""


@patch(f"{TESTED_MODULE}.MP3")
def test_get_one_tag__return_tag_if_id3_with_text(m_mp3):
    # given
    mp3filehandler = Mp3FileHandler("fake_path.mp3")
    mp3filehandler.id3 = Mock()
    fake_tag = Mock()
    fake_tag.text = ["title"]
    mp3filehandler.id3.getall.return_value = [fake_tag]

    # when
    result = mp3filehandler.get_one_tag("title", "text")

    # then
    assert result == "title"


@patch(f"{TESTED_MODULE}.MP3")
def test_get_one_tag__return_tag_if_id3_with_data(m_mp3):
    # given
    mp3filehandler = Mp3FileHandler("fake_path.mp3")
    mp3filehandler.id3 = Mock()
    fake_tag = Mock()
    fake_tag.data = ["data"]
    mp3filehandler.id3.getall.return_value = [fake_tag]

    # when
    result = mp3filehandler.get_one_tag("title", "data")

    # then
    assert result == ["data"]


@patch(f"{TESTED_MODULE}.MP3")
@patch(f"{TESTED_MODULE}.Mp3FileHandler.get_one_tag")
def test_get_tag_research__return_title_artist_and_album(m_get, m_mp3):
    # given
    mp3filehandler = Mp3FileHandler("fake_path.mp3")
    mp3filehandler.id3 = Mock()
    calls = [call("TIT2", "text"), call("TPE1", "text"), call("TALB", "text")]

    # when
    mp3filehandler.get_tag_research()

    # then
    m_get.assert_has_calls(calls=calls, any_order=True)
