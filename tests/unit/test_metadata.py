import unittest
from sdg.dto.metadata import Metadata, Column


class TestMetadata(unittest.TestCase):

    def test_raises_when_column_has_incorrect_parameters(self):
        self.assertRaises(RuntimeError, Column, name='col1', type='random_element', args={"wrong-param": []})

    def test_raises_on_incorrect_format(self):
        self.assertRaises(NotImplementedError, Metadata, file_name='', format='wrong-choice', columns=[])

