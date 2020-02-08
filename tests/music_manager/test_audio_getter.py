import unittest
import sys, os
'''


class MoteurTest(unittest.TestCase):


    def test_check_extension(self):

        moteurtest = moteur.Moteur()
        filename1 = "mp3"
        filename2 = ".okdeo"

        testvalue1 = moteurtest.check_extension(filename1)
        testvalue2 = moteurtest.check_extension(filename2)

        self.assertEqual(testvalue1,True)
        self.assertEqual(testvalue2,False)


    def test_getFile(self):

        moteurtest = moteur.Moteur()
        filename1 = ".okdeo"

        handler = moteurtest.getFile(filename1, "useless")

        self.assertEqual(handler,None)

    def test_get_extension(self):

        moteurtest =moteur.Moteur()
        filename = "ksozkoksz.exten"

        extension = moteurtest.get_extension(filename)


        self.assertEqual(extension,"exten")


if __name__ == '__main__':
    unittest.main()
'''