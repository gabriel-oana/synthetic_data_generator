import unittest
from unittest.mock import patch

from sdg.converter.base_converter import BaseConverter


class TestBaseConverter(unittest.TestCase):

    @patch.multiple(BaseConverter, __abstractmethods__=set())
    def test_create_raises(self):
        base_converter = BaseConverter()
        self.assertRaises(NotImplementedError, base_converter.create)

