from src.audio_mp3_file_handler import Mp3FileHandler


def test_get_extension__return_mp3():
    # given

    # when
    result = Mp3FileHandler.get_extension()

    # then
    assert result == ".mp3"

