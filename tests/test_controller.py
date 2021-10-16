from src.controller import Controller
from unittest.mock import Mock, patch


from gi.repository import Gtk

import gi


gi.require_version("Gtk", "3.0")


TESTED_MODULE = "src.controller"


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


@patch(f"{TESTED_MODULE}.MODEL")
@patch(f"{TESTED_MODULE}.TREE_VIEW")
@patch(f"{TESTED_MODULE}.CrawlerModification")
def test_but_saved_cliqued_run_a_crawler_modification_thread_and_save_modifications(
    m_crawler, m_tree, m_model
):
    # given
    controller = Controller()
    fake_widget = Mock()
    fake_thread = Mock()
    m_crawler.return_value = fake_thread
    controller.is_opened_directory = True

    # when
    controller.but_saved_clicked(fake_widget)

    # then
    m_model.save_modifications_assert_called()
    fake_thread.start.assert_called()
