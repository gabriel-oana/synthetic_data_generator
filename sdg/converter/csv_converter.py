import io
import csv

from sdg.builder.builder import Builder
from sdg.dto.metadata import Metadata
from sdg.converter.base_converter import BaseConverter


class CSVConverter(BaseConverter):

    def __init__(self, metadata: Metadata):
        self.metadata = metadata

    def create(self, rows: int, progress: bool = True, progress_message: str = None, *args, **kwargs) -> str:
        """
        Creates the csv data as a string to be passed to a writer.
        """
        builder = Builder(metadata=self.metadata)
        vals = builder.build_dataset(rows=rows, progress=progress, progress_message=progress_message)

        file_io = io.StringIO()
        writer = csv.writer(file_io, delimiter=self.metadata.separator)
        writer.writerow(vals.columns)
        writer.writerows(vals.values)
        output = file_io.getvalue()
        file_io.close()

        return output
