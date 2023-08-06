import unittest

from alexandria.file import find


class Tests(unittest.TestCase):

    def test_file_management(self):
        print(find.find_file("txt", "resources"))

    def test_file_methods(self):
        pass

    def test_parsers(self):
        pass
