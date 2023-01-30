import unittest
from unittest.mock import patch

from sdg.utils.base_dump import BaseDump


class TestBaseDump(unittest.TestCase):

    @patch.multiple(BaseDump, __abstractmethods__=set())
    def test_create_raises(self):
        base_dump = BaseDump()
        self.assertRaises(NotImplementedError, base_dump.write, path='.', body='str')

