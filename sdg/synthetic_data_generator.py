from typing import Union, Dict
import boto3

from sdg.dto.metadata import Metadata
from sdg.reader.reader import Reader
from sdg.writer.writer import Writer
from sdg.converter.csv_converter import CSVConverter
from sdg.converter.json_converter import JSONConverter


class SDG:

    def __init__(self, metadata: Union[Dict, Metadata, str], s3_client: boto3.client = None):
        self._metadata_path = metadata
        self.s3_client = s3_client
        self.metadata = self._import_metadata()

    def _import_metadata(self):
        reader = Reader()
        metadata = reader.import_metadata(metadata=self._metadata_path)
        return metadata

    def csv_sample(self, rows: int = 10, progress: bool = False):
        csv_converter = CSVConverter(metadata=self.metadata)
        return csv_converter.create(rows=rows, progress=progress)

    def json_sample(self, rows: int = 10, progress: bool = False, orient: str = 'split'):
        json_converter = JSONConverter(metadata=self.metadata)
        return json_converter.create(rows=rows, progress=progress, orient=orient)

    def write(self, path: str, rows: int = None, progress: bool = False, batch_size: int = None,
              use_batches: bool = False, desired_size: int = None, json_orient='split'):
        writer = Writer(metadata=self.metadata, s3_client=self.s3_client)
        writer.write(orient=json_orient, rows=rows, path=path, use_batches=use_batches, batch_size=batch_size,
                     desired_size=desired_size, progress=progress)
