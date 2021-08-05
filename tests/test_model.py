from unittest.mock import Mock, call, patch, ANY

from src import model

TESTED_MODULE = "src.model"


@patch(f"{TESTED_MODULE}.Model.update_list")
def test_update_directory__reset_modifications(mock_update_list):
    # given
    testmodel = model.Model()
    directory = Mock()
    store = Mock()

    # when
    testmodel.update_directory(directory, store)

    # then
    assert testmodel.modification == {}


@patch(f"{TESTED_MODULE}.VIEW")
@patch(f"{TESTED_MODULE}.TREE_VIEW")
@patch(f"{TESTED_MODULE}.Model.update_view")
def test_reset_all__clear_view_modificaton_and_tree(m_update, m_tree, m_view):
    # given
    selection = Mock()
    testmodel = model.Model()

    # when
    testmodel.reset_all(selection)

    # then
    assert testmodel.modification == {}
    m_tree.manage_bold_font.assert_called_with(ANY, add=False)


@patch(f"{TESTED_MODULE}.TREE_VIEW")
@patch(f"{TESTED_MODULE}.get_file_manager")
def test_save_one__reset_modification_for_saved_file(mock_file, m_tree):
    # given
    testmodel = model.Model()
    audio = Mock()
    mock_file.return_value = audio
    selection = Mock()
    testmodel.modification = {
        "fake_file": {
            "title": "new_title",
        }
    }
    selection.get_selected_rows.return_value = ({"file1": ["fake_file"]}, ["file1"])

    # when
    testmodel.save_one(selection)

    # then
    assert testmodel.modification["fake_file"] == {}


@patch(f"{TESTED_MODULE}.TREE_VIEW")
@patch(f"{TESTED_MODULE}.get_file_manager")
def test_save_one__save_modification_on_file(mock_file, m_tree):
    # given
    testmodel = model.Model()
    audio = Mock()
    mock_file.return_value = audio
    selection = Mock()
    testmodel.modification = {
        "fake_file": {
            "title": "new_title",
        }
    }
    selection.get_selected_rows.return_value = ({"file1": ["fake_file"]}, ["file1"])

    # when
    testmodel.save_one(selection)

    # then
    audio.set_tag.assert_called_with("title", "new_title")
    audio.save_modifications.assert_called()


def test_update_tags_dictionary__update_tags_dictionary_when_a_file_is_modified():
    # Arrange
    testmodel = model.Model()
    testmodel.modification = {"testkey": {"album": "a", "artist": "c"}}

    # Act
    testmodel.update_tags_dictionary("testkey")

    # Assert
    assert "a" == testmodel.tags_dictionary["album"]
    assert "c" == testmodel.tags_dictionary["artist"]


def test_check_tag_equal_key_value_return_1_if_tag_is_equal_to_expected_value():
    # Arrange
    testmodel = model.Model()
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
    mymodel = model.Model()
    mymodel.tags_dictionary["title"] = "jojo"

    # When
    mymodel.erase_tag()

    # Then
    for key in mymodel.tags_dictionary:
        assert mymodel.tags_dictionary[key] == ""


@patch(f"{TESTED_MODULE}.VIEW")
@patch(f"{TESTED_MODULE}.Model.update_view")
@patch(f"{TESTED_MODULE}.TREE_VIEW.manage_bold_font")
def test_reset_all_check_erasure_of_tags_modification_on_tree(
    mock_bold, mock_update_view, mock_view
):
    # Given
    testmodel = model.Model()
    testmodel.modification = {"jojo": "jojo"}
    expected_filename = "ost.mp3"
    testmodel.file_name = expected_filename
    selection = {"jaja"}

    # When
    testmodel.reset_all(selection)

    # Then
    assert testmodel.modification == {}
    mock_update_view.assert_called_once_with(selection)
    mock_bold.assert_called_once_with(expected_filename, add=False)


@patch(f"{TESTED_MODULE}.Model.file_modified", return_value=False)
@patch(f"{TESTED_MODULE}.TREE_VIEW.manage_bold_font")
def test_update_modification_name_file__remove_bold_fonts_if_modification_removed(
    mock_bold, mock_file
):
    # Given
    testmodel = model.Model()
    testmodel.modification = {
        "ost.mp4": {
            "title": "naruto",
        },
    }

    # When
    testmodel.update_modification_name_file("ost.mp4", "title", "sasuke")

    # Then
    mock_bold.assert_called_with(["ost.mp4"], add=False)


@patch(f"{TESTED_MODULE}.Model.file_modified", return_value=True)
@patch(f"{TESTED_MODULE}.TREE_VIEW.manage_bold_font")
def test_update_modification_name_file__add_bold_fonts_if_file_modified(
    mock_bold, mock_file
):
    # Given
    testmodel = model.Model()
    testmodel.modification = {
        "ost.mp4": {
            "title": "naruto",
        },
    }

    # When
    testmodel.update_modification_name_file("ost.mp4", "title", "sasuke")

    # Then
    mock_bold.assert_called_with(["ost.mp4"])


@patch(f"{TESTED_MODULE}.Model.file_modified", return_value=True)
@patch(f"{TESTED_MODULE}.TREE_VIEW.manage_bold_font")
def test_set_online_tags__set_tags_found_for_name_file_if_file_already_modified(
    mock1, mock2
):
    # Given
    testmodel = model.Model()
    testmodel.modification = {
        "ost.mp4": {
            "title": "naruto",
        },
    }
    testmodel.data_crawler = Mock()
    testmodel.data_crawler.tag_founds = {
        "ost.mp4": {
            "title": "pain",
        },
    }

    # When
    testmodel.set_online_tags()

    # Then
    assert testmodel.modification["ost.mp4"]["title"] == "pain"


@patch(f"{TESTED_MODULE}.Model.file_modified", return_value=True)
@patch(f"{TESTED_MODULE}.TREE_VIEW.manage_bold_font")
def test_set_online_tags__set_tags_found_for_name_file_if_file_not_modified(
    mock1, mock2
):
    # Given
    testmodel = model.Model()
    testmodel.modification = {}
    testmodel.data_crawler = Mock()
    testmodel.data_crawler.tag_founds = {
        "ost.mp4": {
            "title": "pain",
        },
    }

    # When
    testmodel.set_online_tags()

    # Then
    assert testmodel.modification["ost.mp4"]["title"] == "pain"


@patch(f"{TESTED_MODULE}.TREE_VIEW.manage_bold_font")
@patch(f"{TESTED_MODULE}.get_file_manager")
def test_save_modifications__set_tags_for_each_file_in_modification(
    mock_audio, mock_bold
):
    # Given
    testmodel = model.Model()
    testmodel.modification = {
        "ost.mp4": {
            "title": "naruto",
        },
    }
    audio = Mock()
    mock_audio.return_value = audio

    # When
    testmodel.save_modifications()

    # Then
    audio.set_tag.assert_called_with("title", "naruto")
    assert testmodel.modification == {}


@patch(f"{TESTED_MODULE}.TREE_VIEW.manage_bold_font")
@patch(f"{TESTED_MODULE}.get_file_manager")
def test_save_modifications__remove_bold_fonts_for_each_file_in_modification(
    mock_audio, mock_bold
):
    # Given
    testmodel = model.Model()
    testmodel.modification = {
        "ost.mp4": {
            "title": "naruto",
        },
    }
    audio = Mock()
    mock_audio.return_value = audio

    # When
    testmodel.save_modifications()

    # Then
    mock_bold.assert_called_with(["ost.mp4"], add=False)


@patch(f"{TESTED_MODULE}.TREE_VIEW")
def test_set_data_crawled__update_modification_with_data_scrapped(mock_tree):
    # given
    selection = Mock()
    selection.get_selected_rows.return_value = ("fake_model", ["file"])
    testmodel = model.Model()
    testmodel.update_modifications = Mock()
    testmodel.data_crawler.get_tags = Mock()
    testmodel.data_crawler.get_tags.return_value = {
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


@patch(f"{TESTED_MODULE}.TREE_VIEW")
def test_set_data_crawled__update_modification_with_data_scrapped_if_multiple_files(
    mock_tree,
):
    # given
    selection = Mock()
    selection.get_selected_rows.return_value = ("fake_model", ["file1", "file2"])
    testmodel = model.Model()
    testmodel.update_modifications = Mock()
    testmodel.data_crawler.get_tags = Mock()
    testmodel.data_crawler.get_tags.return_value = {
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
    testmodel = model.Model()
    audio_mock = Mock()
    mock_get_file_manager.return_value = audio_mock
    audio_mock.get_tags.return_value = {
        "title": "fake_title",
        "album": "fake_album",
        "type": "fake type",
    }
    testmodel.modification = {}

    # when
    result = testmodel.file_modified("fake_file")

    # then
    assert result is False


@patch(f"{TESTED_MODULE}.get_file_manager")
def test_file_modified__return_false_if_modif_are_equal_to_file(mock_get_file_manager):
    # given
    testmodel = model.Model()
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
    result = testmodel.file_modified("fake_file")

    # then
    assert result is False


@patch(f"{TESTED_MODULE}.get_file_manager")
def test_file_modified__return_true_if_modifications(mock_get_file_manager):
    # given
    testmodel = model.Model()
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
    result = testmodel.file_modified("fake_file")

    # then
    assert result is True


@patch(f"{TESTED_MODULE}.TREE_VIEW")
def test_update_modifications__if_one_file_modified_not_already_in_modifications_update_modification(
    mock_tree,
):
    # given
    testmodel = model.Model()
    testmodel.file_modified = Mock()
    selection = Mock()
    selection.get_selected_rows.return_value = ({"file1": ["thunder"]}, ["file1"])

    # when
    testmodel.update_modifications(selection, "title", "arto")

    # then
    assert testmodel.modification == {
        "thunder": {
            "title": "arto",
        },
    }


@patch(f"{TESTED_MODULE}.TREE_VIEW")
def test_update_modifications__if_one_file_modified__in_modifications_update_modification(
    mock_tree,
):
    # given
    testmodel = model.Model()
    testmodel.file_modified = Mock()
    selection = Mock()
    selection.get_selected_rows.return_value = ({"file1": ["thunder"]}, ["file1"])
    testmodel.modification = {
        "thunder": {
            "title": "test",
        },
    }

    # when
    testmodel.update_modifications(selection, "title", "arto")

    # then
    assert testmodel.modification == {
        "thunder": {
            "title": "arto",
        },
    }


@patch(f"{TESTED_MODULE}.get_file_manager")
def test_get_tags__return_tags_value_for_one_file(file_manager):
    # given
    gmodel = {"file1": ["fake_file.mp3"]}
    list_iterator = ["file1"]
    testmodel = model.Model()
    audio = Mock()
    file_manager.return_value = audio
    testmodel.modification = {
        "fake_file.mp3": {
            "title": "fake_title",
            "album": "fake_album",
            "length": "1m and 33s",
        }
    }

    # when
    output = testmodel.get_tags(gmodel, list_iterator)

    # then
    assert output == 0
    assert testmodel.tags_dictionary["title"] == "fake_title"
    assert testmodel.tags_dictionary["album"] == "fake_album"
    assert testmodel.tags_dictionary["length"] == "1m and 33s"


@patch(f"{TESTED_MODULE}.get_file_manager")
def test_get_tags__return_tags_value_for_multiple_files(file_manager):
    # given
    gmodel = {"file1": ["fake_file.mp3"], "file2": ["fake_second_file.mp3"]}
    list_iterator = ["file1", "file2"]
    testmodel = model.Model()
    audio = Mock()
    file_manager.return_value = audio
    testmodel.modification = {
        "fake_file.mp3": {
            "title": "fake_title",
            "album": "fake_album",
            "length": "1m and 33s",
        },
        "fake_second_file.mp3": {
            "title": "fake_title2",
            "album": "fake_album",
            "length": "2m",
        },
    }

    # when
    output = testmodel.get_tags(gmodel, list_iterator)

    # then
    assert output == 1
    assert testmodel.tags_dictionary["title"] == ""
    assert testmodel.tags_dictionary["album"] == "fake_album"
    assert testmodel.tags_dictionary["length"] == ""


def test_wait_for_mbz___call_get_tags_until_selection_changes_then_display_it():
    # given

    # when

    # then
    pass


def test_update_view__clean_all_get_tags_and_display_them():
    # given


    # when

    # then
    pass
