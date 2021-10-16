from unittest.mock import Mock, call, patch

from src.model import Model

TESTED_MODULE = "src.model"


def test_reset_all__clear_view_modificaton_and_tree():
    # given
    model = Model()
    model.modification = {
        "fake": "",
    }

    # when
    model.reset_all()

    # then
    assert model.modification == {}


def test_update_tags_dictionary__update_tags_dictionary_when_a_file_is_modified():
    # Arrange
    testmodel = Model()
    testmodel.modification = {"testkey": {"album": "a", "artist": "c"}}

    # Act
    testmodel.update_tags_dictionary_with_modification("testkey")

    # Assert
    assert "a" == testmodel.tags_dictionary["album"]
    assert "c" == testmodel.tags_dictionary["artist"]


def test_check_tag_equal_key_value_return_1_if_tag_is_equal_to_expected_value():
    # Arrange
    testmodel = Model()
    testmodel.modification = {"testkey": {"album": "nqnt", "artist": "vald"}}

    # Act
    value_test1 = testmodel.check_tag_equal_key_value(
        0, "", "testkey", "artist", "vald"
    )
    value_test2 = testmodel.check_tag_equal_key_value(
        1, "xeu", "testkey", "album", "xeu"
    )

    # Assert
    assert value_test1 == 1
    assert value_test2 == 0


def test_erase_tag_results_in_erasing_tags_dictionary():
    # Given
    mymodel = Model()
    mymodel.tags_dictionary["title"] = "jojo"

    # When
    mymodel.erase_tag()

    # Then
    for key in mymodel.tags_dictionary:
        assert mymodel.tags_dictionary[key] == ""


@patch(f"{TESTED_MODULE}.get_file_manager")
def test_save_modifications__set_tags_for_each_file_in_modification(mock_audio):
    # Given
    testmodel = Model()
    testmodel.modification = {
        "ost.mp4": {
            "title": "naruto",
        },
    }
    audio = Mock()
    mock_tree = Mock()
    mock_audio.return_value = audio

    # When
    testmodel.save_modifications(mock_tree)

    # Then
    audio.set_tag.assert_called_with("title", "naruto")
    assert testmodel.modification == {"ost.mp4": {}}


@patch(f"{TESTED_MODULE}.get_file_manager")
def test_save_modifications__remove_bold_fonts_for_each_file_in_modification(
    mock_audio,
):
    # Given
    testmodel = Model()
    testmodel.modification = {
        "ost.mp4": {
            "title": "naruto",
        },
    }
    audio = Mock()
    mock_tree = Mock()
    mock_audio.return_value = audio

    # When
    testmodel.save_modifications(mock_tree)

    # Then
    mock_tree.manage_bold_font.assert_called_with(["ost.mp4"], add=False)


@patch(f"{TESTED_MODULE}.DATA_CRAWLER")
def test_set_data_crawled__update_modification_with_data_scrapped(mock_data_crawler):
    # given
    selection = Mock()
    selection.get_selected_rows.return_value = ("fake_model", ["file"])
    testmodel = Model()
    testmodel.update_modifications = Mock()
    mock_data_crawler.get_tags = Mock()
    mock_data_crawler.get_tags.return_value = {
        "title": "test",
        "album": "",
        "year": "2020",
        "genre": "pop",
        "cover": "cov",
    }

    calls = [
        call(selection, "title", "test"),
        call(selection, "year", "2020"),
        call(selection, "genre", "pop"),
        call(selection, "cover", "cov"),
    ]

    # when
    testmodel.set_data_crawled(selection)

    # then
    testmodel.update_modifications.assert_has_calls(calls, any_order=True)


@patch(f"{TESTED_MODULE}.DATA_CRAWLER")
def test_set_data_crawled__update_modification_with_data_scrapped_if_multiple_files(
    mock_data_crawler,
):
    # given
    selection = Mock()
    selection.get_selected_rows.return_value = ("fake_model", ["file1", "file2"])
    testmodel = Model()
    testmodel.update_modifications = Mock()
    mock_data_crawler.get_tags = Mock()
    mock_data_crawler.get_tags.return_value = {
        "title": "test",
        "album": "",
        "year": "2020",
        "genre": "pop",
        "cover": "cov",
    }

    calls = [
        call(selection, "title", "test"),
        call(selection, "year", "2020"),
        call(selection, "genre", "pop"),
        call(selection, "cover", "cov"),
    ]

    # when
    testmodel.set_data_crawled(selection)

    # then
    testmodel.update_modifications.assert_has_calls(calls, any_order=True)


@patch(f"{TESTED_MODULE}.get_file_manager")
def test_file_modified__return_false_if_no_modification(mock_get_file_manager):
    # given
    testmodel = Model()
    audio_mock = Mock()
    mock_get_file_manager.return_value = audio_mock
    audio_mock.get_tags.return_value = {
        "title": "fake_title",
        "album": "fake_album",
        "type": "fake type",
    }
    testmodel.modification = {}

    # when
    result = testmodel.is_file_modified("fake_file")

    # then
    assert result is False


@patch(f"{TESTED_MODULE}.get_file_manager")
def test_file_modified__return_false_if_modif_are_equal_to_file(mock_get_file_manager):
    # given
    testmodel = Model()
    audio_mock = Mock()
    mock_get_file_manager.return_value = audio_mock
    audio_mock.get_tags.return_value = {
        "title": "fake_title",
        "album": "fake_album",
        "type": "fake type",
    }
    testmodel.modification = {
        "fake_file": {
            "title": "fake_title",
            "album": "fake_album",
            "type": "fake type",
        },
    }

    # when
    result = testmodel.is_file_modified("fake_file")

    # then
    assert result is False


@patch(f"{TESTED_MODULE}.get_file_manager")
def test_file_modified__return_true_if_modifications(mock_get_file_manager):
    # given
    testmodel = Model()
    audio_mock = Mock()
    mock_get_file_manager.return_value = audio_mock
    audio_mock.get_tags.return_value = {
        "title": "fake_title",
        "album": "fake_album",
        "type": "fake type",
    }
    testmodel.modification = {
        "fake_file": {
            "title": "fake_modified_title",
            "album": "fake_album",
            "type": "fake type",
        },
    }

    # when
    result = testmodel.is_file_modified("fake_file")

    # then
    assert result is True


def test_update_modifications__if_one_file_modified_not_already_in_modifications_update_modification():
    # given
    testmodel = Model()
    testmodel.is_file_modified = Mock()

    # when
    testmodel.update_modifications(["fake_file.mp3"], "title", "arto")

    # then
    assert testmodel.modification == {
        "fake_file.mp3": {
            "title": "arto",
        },
    }


def test_update_modifications__if_one_file_modified__in_modifications_update_modification():
    # given
    testmodel = Model()
    testmodel.is_file_modified = Mock()
    testmodel.modification = {
        "fake_file.mp3": {
            "title": "test",
        },
    }

    # when
    testmodel.update_modifications(["fake_file.mp3"], "title", "arto")

    # then
    assert testmodel.modification == {
        "fake_file.mp3": {
            "title": "arto",
        },
    }
