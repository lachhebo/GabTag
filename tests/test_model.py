from unittest.mock import patch

from src import model

TESTED_MODULE = "src.model"


def test_check_dictionary_update_tags_dictionary_when_a_file_is_modified():
    # Arrange
    testmodel = model.Model()
    testmodel.modification = {"testkey": {"album": "a", "artist": "c"}}

    # Act
    testmodel.check_dictionary("testkey")

    # Assert
    assert "a" == testmodel.tags_dictionary["album"]["value"]
    assert "c" == testmodel.tags_dictionary["artist"]["value"]


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
    mymodel.tags_dictionary["title"]["value"] = "jojo"

    # When
    mymodel.erase_tag()

    # Then
    for key in mymodel.tags_dictionary:
        assert mymodel.tags_dictionary[key]["value"] == ""


@patch(f"{TESTED_MODULE}.VIEW")
@patch(f"{TESTED_MODULE}.Model.update_view")
@patch(f"{TESTED_MODULE}.TREE_VIEW.remove_bold_font")
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
    mock_bold.assert_called_once_with(expected_filename)


def test_set_data_lyrics__get_and_set_lyrics_when_one_line_involved():
    pass


def test_set_data_lyrics__get_and_set_lyrics_when_multiple_lines_involved():
    pass


def test_update_modification_name_file__remove_bold_fonts_if_modification_removed():
    pass


def test_update_modification_name_file__add_bold_fonts_if_file_modified():
    pass


def test_set_online_tags__set_tags_found_for_name_file_if_file_already_modified():
    pass


def test_set_online_tags__set_tags_found_for_name_file_if_file_not_modified():
    pass


def test_save_modifications__set_tags_for_each_file_in_modification():
    pass


def test_save_modifications__remove_bold_fonts_for_each_file_in_modification():
    pass


def test_save_modifications__reset_modifications():
    pass


def test_set_data_crawled__update_modification_with_data_scrapped_if_one_file():
    pass


def test_set_data_crawled__update_modification_with_data_scrapped_if_multiple_files():
    pass


def test_file_modified__return_true_if_tag_is_different_from_value_in_modification():
    pass


def test_file_modified__return_true_if_tag_not_in_modifications():
    pass


def test_file_modified__return_true_if_tag_in_modification_are_equal_to_tags():
    pass


def test_update_modifications__if_one_file_modified_already_in_modifications_update_modification():
    pass


def test_update_modifications__if_one_file_modified_already_not_in_modifications_update_modification():
    pass


def test_update_modifications__if_one_file_is_modified_add_bold_fonts():
    pass


def test_update_modifications__if_one_file_modification_removed_add_bold_fonts():
    pass


def test_update_modifications__if_multiple_files_modified_already_in_modifications_update_modification():
    pass


def test_update_modifications__if_multiple_files__modified_already_not_in_modifications_update_modification():
    pass


def test_update_modifications__if_multiple_files__is_modified_add_bold_fonts():
    pass


def test_update_modifications__if_multiple_files_modification_removed_add_bold_fonts():
    pass


def test_wait_for_lyrics___call_get_lyrics_until_selection_changes_then_display_it():
    pass


def test_wait_for_mbz___call_get_tags_until_selection_changes_then_display_it():
    pass


def test_update_view__clean_all_get_tags_and_display_them():
    pass
