import os
import yaml
import json
import shutil
import unittest
from pathlib import Path

from sdg.reader.reader import Reader
from sdg.dto.metadata import Metadata


class TestReader(unittest.TestCase):

    def setUp(self) -> None:
        # Create JSON and YAML metadata
        self.metadata = {
            "format": "csv",
            "file_name": "test-file-name",
            "separator": ",",
            "seed": 50,
            "columns": [
                {
                    "name": "column_1",
                    "type": "string",
                    "null_probability": 0,
                    "unique": False,
                    "locale": "en-US",
                    "seed": 1,
                    "args": {
                        "min_chars": 8,
                        "max_chars": 16
                    }
                }
            ]
        }

        self.temp_path = f'{os.path.abspath("")}/test-files'
        self.temp_file = f"{self.temp_path}/metadata"

        # Check if the path exists otherwise create it.
        if not os.path.exists(self.temp_path):
            Path(self.temp_path).mkdir(parents=True, exist_ok=True)

        # Write the files as yaml, yml and json
        with open(f"{self.temp_file}.json", 'w+') as f:
            f.write(json.dumps(self.metadata))

        with open(f"{self.temp_file}.yml", 'w+') as f:
            f.write(yaml.dump(self.metadata))

        with open(f"{self.temp_file}.yaml", 'w+') as f:
            f.write(yaml.dump(self.metadata))

    def test_import_metadata_json(self):
        reader = Reader()
        metadata = reader.import_metadata(metadata=f"{self.temp_file}.json")
        self.assertIsInstance(metadata, Metadata)

    def test_import_metadata_yaml(self):
        reader = Reader()
        metadata = reader.import_metadata(metadata=f"{self.temp_file}.yaml")
        self.assertIsInstance(metadata, Metadata)

    def test_import_metadata_yml(self):
        reader = Reader()
        metadata = reader.import_metadata(metadata=f"{self.temp_file}.yml")
        self.assertIsInstance(metadata, Metadata)

    def test_import_metadata_raises_on_wrong_file_format(self):
        reader = Reader()
        self.assertRaises(RuntimeError, reader.import_metadata, metadata=f"{self.temp_file}.xml")

    def test_import_metadata_raises_of_wrong_type(self):
        reader = Reader()
        self.assertRaises(RuntimeError, reader.import_metadata, metadata=[])

    def test_import_metadata_dict(self):
        reader = Reader()
        metadata = reader.import_metadata(self.metadata)
        self.assertIsInstance(metadata, Metadata)

    def test_import_metadata_object(self):

        metadata = Metadata(
            file_name='test-file',
            format='csv',
            columns=[]
        )

        reader = Reader()
        metadata = reader.import_metadata(metadata)
        self.assertIsInstance(metadata, Metadata)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_path)
