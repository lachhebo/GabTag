import unittest
import sys, os
from gabtag import MP3Handler


class MP3HandlerTest(unittest.TestCase):

    def test_get_one_tag(self):
        '''
        entry : id3_nametag,data_type
        A function to return the first tag of an id3 label
        '''
        pass

    def test_getTag(self):
        '''
        entry : s
        We handle tag using a switch, it is working well because it is basically the structure.
        '''
        pass

    def test_check_tag_existence(self):
        #audio = MP3Handler()
        #result = check_tag_existence(key)

        # assert :
        pass

    def test_setTag(self):
        #audio = MP3Handler()
        #result = setTag(tag_key,tag_value)
        pass

    def test_savemodif(self):
        result = 1
        pass

if __name__ == '__main__':
    unittest.main()
