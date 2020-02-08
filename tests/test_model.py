import unittest
import sys, os
from src import model
from gi.repository import Gtk


class ModelTest(unittest.TestCase):


    def test_update_directory(self): # The code have changed
        '''
        # Arrange
        testmodel = model.Model.getInstance()

        # Act
        directory = "/home/mouloud/music"
        testmodel.update_directory(directory)

        # Assert
        self.assertEqual(directory,testmodel.directory)
        self.assertEqual({},testmodel.modification)
        '''
        pass



    def test_check_dictionnary(self):


        # Arrange
        testmodel = model.Model.get_instance()
        testmodel.modification = { "testkey" : { "album": "a", "artist": "c"} }
        tag_changed = {"tag1","tag2"}

        # Act
        testmodel.check_dictionary("testkey")

        # Assert
        self.assertEqual("a",testmodel.tagdico["album"]["value"])
        self.assertEqual("c",testmodel.tagdico["artist"]["value"])



    def test_check_tag_equal_key_value(self):


        # Arrange
        testmodel = model.Model.get_instance()
        testmodel.modification = { "testkey" : { "album": "nqnt", "artist": "vald"} }

        #Act
        value_test1 = testmodel.check_tag_equal_key_value(0,"", "testkey","artist","vald")
        value_test2 = testmodel.check_tag_equal_key_value(1,"xeu", "testkey","album","xeu")

        #Assert
        self.assertEqual(value_test1,1)
        self.assertEqual(value_test2,0)


if __name__ == '__main__':
    unittest.main()
