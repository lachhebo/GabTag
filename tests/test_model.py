import unittest
import sys, os
from src import model
from gi.repository import Gtk


class ModelTest(unittest.TestCase):


    def test_update_directory(self):

        # Arrange

        testmodel = model.Model.getInstance()

        # Act

        directory = "/home/mouloud/music"
        testmodel.update_directory(directory)

        # Assert

        self.assertEqual(directory,testmodel.directory)
        self.assertEqual({},testmodel.modification)


    def test_update_modifications(self):
        '''
        # Arrange
        testmodel = model.Model.getInstance()
        testmodel.modification = { "testkey" : { "tag1": "a"} }
        selection = Gtk.TreeSelection()
        print(dir(selection))
        # Act

        testmodel.update_modifications(selection, "tag1", "b")
        testmodel.update_modifications(selection, "tag2", "a")

        selection = ... #TODO
        testmodel.update_modifications(selection, "tag1", "c")


        selection = ... #TODO

        testmodel.update_modifications(selection, "tag1", "i")
        testmodel.update_modifications(selection, "tag2", "f")
        testmodel.update_modifications(selection, "tag3", "g")
        '''
        # Assert


    def test_check_dictionnary(self):
        # Arrange

        testmodel = model.Model.getInstance()

        testmodel.modification = { "testkey" : { "album": "a", "artist": "c"} }
        tag_changed = {"tag1","tag2"}

        # Act

        testmodel.check_dictionnary("testkey")

        # Assert

        self.assertEqual("a",testmodel.tagdico["album"]["value"])
        self.assertEqual("c",testmodel.tagdico["artist"]["value"])



if __name__ == '__main__':
    unittest.main()
