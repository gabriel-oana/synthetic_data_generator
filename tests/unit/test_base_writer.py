import unittest

from sdg.writer.base_writer import BaseWriter
from sdg.dto.metadata import Metadata, Column
from sdg.converter.csv_converter import CSVConverter

class TestBaseWriter(unittest.TestCase):

    def setUp(self) -> None:
        column1 = Column(
            name='col1',
            type='string',
            unique=True,
            seed=1
        )

        metadata = Metadata(
            columns=[column1],
            file_name='test',
            format='json',
        )

        converter = CSVConverter(metadata=metadata)
        self.base_writer = BaseWriter(
            converter=converter,
            path="local_path",
            metadata=metadata
        )

    def test_validate_desired_size_too_big(self):
        self.assertWarns(UserWarning, self.base_writer.validate, desired_size=2000, use_batches=False)

    def test_validate_rows_too_big(self):
        self.assertWarns(UserWarning, self.base_writer.validate, rows=1000000000, use_batches=False)
