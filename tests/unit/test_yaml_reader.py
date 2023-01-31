import os
import unittest

from sdg.reader.yaml_reader import YAMLReader


class TestYamlReader(unittest.TestCase):

    def setUp(self) -> None:
        location = 'tests/data_files'
        file_name = 'broken.yaml'
        self.file_location = f"{location}/{file_name}"

        with open(self.file_location, 'w+') as f:
            f.write("something: '")

    def test_reader_raises_on_wrong_format(self):
        yaml_reader = YAMLReader()
        self.assertRaises(RuntimeError, yaml_reader.read, file=self.file_location)

    def tearDown(self) -> None:
        os.remove(self.file_location)