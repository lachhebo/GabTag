from unittest.mock import patch

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
