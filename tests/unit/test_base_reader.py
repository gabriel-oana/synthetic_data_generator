import unittest
from unittest.mock import patch

from sdg.reader.base_reader import BaseReader


class TestBaseReader(unittest.TestCase):

    @patch.multiple(BaseReader, __abstractmethods__=set())
    def test_create_raises(self):
        base_reader = BaseReader()
        self.assertRaises(NotImplementedError, base_reader.read)

