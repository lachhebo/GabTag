from src.event_machine import EventMachine
from unittest.mock import Mock, patch


from gi.repository import Gtk

import gi


gi.require_version("Gtk", "3.0")


TESTED_MODULE = "src.event_machine"

# title


@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_title_change_run_update_modifications(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 1

    # when
    event_machine.on_title_changed(widget)

    # then
    assert event_machine.is_real_selection == 1
    mock_modif.assert_called_with("title", "fake_text")


@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_title_change__doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 0

    # when
    event_machine.on_title_changed(widget)

    # then
    mock_modif.assert_not_called()


# artist


@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_artist_change_run_update_modifications(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 1

    # when
    event_machine.on_artist_changed(widget)

    # then
    assert event_machine.is_real_selection == 1
    mock_modif.assert_called_with("artist", "fake_text")


@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_artist_change__doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 0

    # when
    event_machine.on_artist_changed(widget)

    # then
    mock_modif.assert_not_called()


# album


@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_album_change_run_update_modifications(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 1

    # when
    event_machine.on_album_changed(widget)

    # then
    assert event_machine.is_real_selection == 1
    mock_modif.assert_called_with("album", "fake_text")


@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_album_change__doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 0

    # when
    event_machine.on_album_changed(widget)

    # then
    mock_modif.assert_not_called()


# genre


@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_genre_change_run_update_modifications(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 1

    # when
    event_machine.on_type_changed(widget)

    # then
    assert event_machine.is_real_selection == 1
    mock_modif.assert_called_with("genre", "fake_text")


@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_genre_change__doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 0

    # when
    event_machine.on_type_changed(widget)

    # then
    mock_modif.assert_not_called()


# track

@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_track_change_run_update_modifications(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 1

    # when
    event_machine.on_track_changed(widget)

    # then
    assert event_machine.is_real_selection == 1
    mock_modif.assert_called_with("track", "fake_text")


@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_track_change__doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 0

    # when
    event_machine.on_track_changed(widget)

    # then
    mock_modif.assert_not_called()


# year

@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_year_change_run_update_modifications(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 1

    # when
    event_machine.on_year_changed(widget)

    # then
    assert event_machine.is_real_selection == 1
    mock_modif.assert_called_with("year", "fake_text")


@patch(f"{TESTED_MODULE}.Controller.react_to_user_modif")
def test_on_year_change__doesnt_run_update_modifications_if_no_selection(mock_modif):
    # given
    event_machine = EventMachine()
    widget = Mock()
    widget.get_text = Mock()
    widget.get_text.return_value = "fake_text"
    event_machine.is_real_selection = 0

    # when
    event_machine.on_year_changed(widget)

    # then
    mock_modif.assert_not_called()


@patch(f"{TESTED_MODULE}.Controller")
@patch(f"{TESTED_MODULE}.get_filenames_from_selection")
@patch(f"{TESTED_MODULE}.add_filters")
@patch(f"{TESTED_MODULE}.MODEL")
@patch(f"{TESTED_MODULE}.Gtk.FileChooserDialog")
def test_on_load_cover_clicked__run_update_modifcations_and_update_view_if_dialog_return_ok(
    mock_d, mock_model, m_filters, m_filenames, m_controller
):
    # given
    mock_dialog = Mock()
    mock_d.return_value = mock_dialog
    mock_dialog.run.return_value = Gtk.ResponseType.OK
    event_machine = EventMachine()
    event_machine.is_real_selection = 1
    widget = Mock()

    # when
    event_machine.on_load_cover_clicked(widget)

    # then

    mock_model.update_modifications.assert_called()
    m_controller.update_view.assert_called()


@patch(f"{TESTED_MODULE}.get_filenames_from_selection")
@patch(f"{TESTED_MODULE}.Controller")
def test_selected_changed_update_the_view(mock_model, moc_filenames):
    # given
    event_machine = EventMachine()
    event_machine.is_real_selection = 1
    selection = Mock()

    # when
    event_machine.on_selected_changed(selection)

    # then
    mock_model.update_view.assert_called()


@patch(f"{TESTED_MODULE}.get_filenames_from_selection")
@patch(f"{TESTED_MODULE}.Controller")
def test_selected_changed_doesnt_update_the_view_if_no_selection(mock_model, moc_filenames):
    # given
    event_machine = EventMachine()
    event_machine.is_real_selection = 0
    selection = Mock()

    # when
    event_machine.on_selected_changed(selection)

    # then
    mock_model.update_view.assert_not_called()


@patch(f"{TESTED_MODULE}.get_filenames_from_selection")
@patch(f"{TESTED_MODULE}.Controller")
@patch(f"{TESTED_MODULE}.MODEL")
def test_on_set_mbz__update_the_view_if_selection_changed(m_model, m_controller, m_filenames):
    # given
    event_machine = EventMachine()
    event_machine.is_real_selection = 1
    widget = Mock()

    # when
    event_machine.on_set_mbz(widget)

    # then
    m_controller.update_view.assert_called()
    m_model.set_data_crawled.assert_called()


@patch(f"{TESTED_MODULE}.get_filenames_from_selection")
@patch(f"{TESTED_MODULE}.Controller")
@patch(f"{TESTED_MODULE}.MODEL")
def test_on_set_mbz__update_the_view_if_no_selection(m_model, m_controller, m_filenames):
    # given
    event_machine = EventMachine()
    event_machine.is_real_selection = 0
    widget = Mock()

    # when
    event_machine.on_set_mbz(widget)

    # then
    m_controller.update_view.assert_not_called()
    m_model.set_data_crawled.assert_not_called()


@patch(f"{TESTED_MODULE}.get_filenames_from_selection")
@patch(f"{TESTED_MODULE}.Controller")
@patch(f"{TESTED_MODULE}.SELECTION")
@patch(f"{TESTED_MODULE}.MODEL")
@patch(f"{TESTED_MODULE}.DIR_MANAGER")
def test_on_set_online_tags__set_the_online_tags_using_model_data_and_update_view(m_dir_manager, m_model, m_selection, m_controller, _):
    # given
    event_machine = EventMachine()
    event_machine.is_real_selection = 1

    m_dir_manager.is_opened_directory = True
    widget = Mock()

    # when
    event_machine.on_set_online_tags(widget)

    # then
    m_model.set_online_tags.assert_called()
    m_controller.update_view.assert_called()


@patch(f"{TESTED_MODULE}.get_filenames_from_selection")
@patch(f"{TESTED_MODULE}.Controller")
@patch(f"{TESTED_MODULE}.SELECTION")
@patch(f"{TESTED_MODULE}.MODEL")
@patch(f"{TESTED_MODULE}.DIR_MANAGER")
def test_on_set_online_tags__does_notset_the_online_tags_using_model_data_and_update_view_if_no_selection(m_dir_manager, m_model, m_selection, m_controller, _):
    # given
    event_machine = EventMachine()
    event_machine.is_real_selection = 0

    m_dir_manager.is_opened_directory = True
    widget = Mock()

    # when
    event_machine.on_set_online_tags(widget)

    # then
    m_model.set_online_tags.assert_not_called()
    m_controller.update_view.assert_not_called()


@patch(f"{TESTED_MODULE}.Controller")
@patch(f"{TESTED_MODULE}.DIR_MANAGER")
def test_on_but_saved_clicked__start_modification_thread(m_dir_manager, m_controller):
    # given
    event_machine = EventMachine()
    m_dir_manager.is_opened_directory = True
    widget = Mock()

    # when
    event_machine.on_but_saved_clicked(widget)

    # then
    m_controller.crawl_thread_modification.assert_called()
