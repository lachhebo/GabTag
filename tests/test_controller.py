from unittest.mock import patch, Mock

import gi

from src.controller import Controller

gi.require_version("Gtk", "3.0")


TESTED_MODULE = "src.controller"


@patch(f"{TESTED_MODULE}.DIR_MANAGER")
@patch(f"{TESTED_MODULE}.TREE_VIEW")
@patch(f"{TESTED_MODULE}.MODEL")
def test_update_directory__reset_modifications(m_model, m_tree, m_dir):
    # given
    controller = Controller()
    fake_directory = "fake"

    # when
    controller.update_directory(fake_directory)

    # then
    m_model.reset_all.assert_called()


@patch(f"{TESTED_MODULE}.VIEW")
@patch(f"{TESTED_MODULE}.MODEL")
def test_reset_all__erase_view_and_model(m_model, m_view):
    # given
    controller = Controller()

    # when
    controller.reset_all()

    # then
    m_model.reset_all.assert_called()
    m_view.erase.assert_called()


@patch(f"{TESTED_MODULE}.TREE_VIEW")
@patch(f"{TESTED_MODULE}.MODEL")
def test_reset_one__erase_view_and_model(m_model, m_tree_view):
    # given
    controller = Controller()

    # when
    controller.reset_one(["fake_file.mp3"])

    # then
    m_model.reset.assert_called()
    m_tree_view.manage_bold_font.assert_called_with(["fake_file.mp3"], add=False)


@patch(f"{TESTED_MODULE}.TREE_VIEW")
@patch(f"{TESTED_MODULE}.CrawlerModification")
@patch(f"{TESTED_MODULE}.MODEL")
def test_crawl_thread_modification__erase_view_and_model(m_model, m_crawl, m_tree_view):
    # given
    controller = Controller()
    m_crawl_ins = Mock()
    m_crawl.return_value = m_crawl_ins

    # when
    controller.crawl_thread_modification()

    # then
    m_crawl_ins.start.assert_called()
    m_model.save_modifications.assert_called()


@patch(f"{TESTED_MODULE}.TREE_VIEW")
@patch(f"{TESTED_MODULE}.get_filenames_from_selection")
@patch(f"{TESTED_MODULE}.MODEL")
@patch(f"{TESTED_MODULE}.CrawlerModification")
def test_save_some_files__erase_view_and_model(m_crawl, m_model, m_get, m_tree_view):
    # given
    controller = Controller()
    m_crawl_ins = Mock()
    m_crawl.return_value = m_crawl_ins

    # when
    controller.save_some_files()

    # then
    m_crawl_ins.start.assert_called()
    m_model.save_modifications.assert_called()


@patch(f"{TESTED_MODULE}.Controller")
@patch(f"{TESTED_MODULE}.get_filenames_from_selection")
@patch(f"{TESTED_MODULE}.CrawlerModification")
def test_reset_some_files__erase_view_and_model(m_crawl, m_get, m_controller):
    # given
    controller = Controller()
    m_crawl_ins = Mock()
    m_crawl.return_value = m_crawl_ins

    # when
    controller.reset_some_files()

    # then
    m_controller.reset_one.assert_called()
