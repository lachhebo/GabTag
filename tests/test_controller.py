from src.controller import Controller
from unittest.mock import Mock, patch


from gi.repository import Gtk

import gi


gi.require_version("Gtk", "3.0")

from src import controller

TESTED_MODULE = "src.controller"


# title


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_title_change_run_update_modifications(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 1

    # when
    controller.title_changed(widget)

    # then
    assert controller.is_real_selection == 1
    mock_modif.assert_called()


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_title_change_doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 0

    # when
    controller.title_changed(widget)

    # then
    mock_modif.assert_not_called()


# artist


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_artist_change_run_update_modifications(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 1

    # when
    controller.artist_changed(widget)

    # then
    assert controller.is_real_selection == 1
    mock_modif.assert_called()


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_artist_change_doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 0

    # when
    controller.artist_changed(widget)

    # then
    mock_modif.assert_not_called()


# album


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_album_change_run_update_modifications(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 1

    # when
    controller.album_changed(widget)

    # then
    assert controller.is_real_selection == 1
    mock_modif.assert_called()


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_artist_change_doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 0

    # when
    controller.album_changed(widget)

    # then
    mock_modif.assert_not_called()


# type


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_type_change_run_update_modifications(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 1

    # when
    controller.type_changed(widget)

    # then
    assert controller.is_real_selection == 1
    mock_modif.assert_called()


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_type_change_doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 0

    # when
    controller.type_changed(widget)

    # then
    mock_modif.assert_not_called()


# track


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_track_change_run_update_modifications(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 1

    # when
    controller.track_changed(widget)

    # then
    assert controller.is_real_selection == 1
    mock_modif.assert_called()


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_track_change_doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 0

    # when
    controller.track_changed(widget)

    # then
    mock_modif.assert_not_called()


# year


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_year_change_run_update_modifications(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 1

    # when
    controller.year_changed(widget)

    # then
    assert controller.is_real_selection == 1
    mock_modif.assert_called()


@patch(f"{TESTED_MODULE}.MODEL.update_modifications")
def test_year_change_doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    controller = Controller()
    widget = Mock()
    controller.is_real_selection = 0

    # when
    controller.year_changed(widget)

    # then
    mock_modif.assert_not_called()


@patch(f"{TESTED_MODULE}.add_filters")
@patch(f"{TESTED_MODULE}.MODEL")
@patch(f"{TESTED_MODULE}.Gtk.FileChooserDialog")
def test_load_cover_clicked__run_updata_modifcations_and_update_view_if_dialog_return_ok(
    mock_d, mock_model, m_filters
):
    # given
    mock_dialog = Mock()
    mock_d.return_value = mock_dialog
    mock_dialog.run.return_value = Gtk.ResponseType.OK
    controller = Controller()
    controller.is_real_selection = 1
    widget = Mock()

    # when
    controller.load_cover_clicked(widget)

    # then

    mock_model.update_modifications.assert_called()
    mock_model.update_view.assert_called()


@patch(f"{TESTED_MODULE}.add_filters")
@patch(f"{TESTED_MODULE}.MODEL")
@patch(f"{TESTED_MODULE}.Gtk.FileChooserDialog")
def test_load_cover_clicked__dont_run_update_modifcations_and_update_view_if_dialog_return_ok(
    mock_d, mock_model, m_filters
):
    # given
    mock_dialog = Mock()
    mock_d.return_value = mock_dialog
    mock_dialog.run.return_value = Gtk.ResponseType.CANCEL
    controller = Controller()
    controller.is_real_selection = 1
    widget = Mock()

    # when
    controller.load_cover_clicked(widget)

    # then

    mock_model.update_modifications.assert_not_called()
    mock_model.update_view.assert_not_called()


@patch(f"{TESTED_MODULE}.MODEL")
def test_selected_changed_update_the_view(mock_model):
    # given
    controller = Controller()
    controller.is_real_selection = 1
    selection = Mock()

    # when
    controller.selected_changed(selection)

    # then
    mock_model.update_view.assert_called()


@patch(f"{TESTED_MODULE}.MODEL")
def test_selected_changed_doesnt_update_the_view_if_no_selection(mock_model):
    # given
    controller = Controller()
    controller.is_real_selection = 0
    selection = Mock()

    # when
    controller.selected_changed(selection)

    # then
    mock_model.update_view.assert_not_called()


@patch(f"{TESTED_MODULE}.MODEL")
def test_on_set_mbz__update_the_view_if_selection_changed(mock_model):
    # given
    controller = Controller()
    controller.is_real_selection = 1
    widget = Mock()

    # when
    controller.on_set_mbz(widget)

    # then
    mock_model.update_view.assert_called()
    mock_model.set_data_crawled.assert_called()


@patch(f"{TESTED_MODULE}.MODEL")
def test_on_set_mbz__doesnt_update_the_view_if_no_selection(mock_model):
    # given
    controller = Controller()
    controller.is_real_selection = 0
    widget = Mock()

    # when
    controller.on_set_mbz(widget)

    # then
    mock_model.update_view.assert_not_called()
    mock_model.set_data_crawled.assert_not_called()


@patch(f"{TESTED_MODULE}.MODEL")
def test_on_set_online_tags__set_the_online_tags_using(mock_model):
    # given
    controller = Controller()
    controller.is_real_selection = 1
    controller.is_opened_directory = True
    controller.selectioned = Mock()
    widget = Mock()

    # when
    controller.on_set_online_tags(widget)

    # then
    mock_model.update_view.assert_called()


@patch(f"{TESTED_MODULE}.MODEL")
def test_on_set_online_tags__doesnt_update_the_view_if_no_selection(mock_model):
    # given
    controller = Controller()
    controller.is_real_selection = 0
    widget = Mock()

    # when
    controller.on_set_online_tags(widget)

    # then
    mock_model.update_view.assert_not_called()
