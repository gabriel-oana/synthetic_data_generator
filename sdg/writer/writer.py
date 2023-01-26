import boto3
from sdg.dto.metadata import Metadata
from sdg.writer.csv_writer import CSVWriter
from sdg.writer.json_writer import JSONWriter


class Writer:

    def __init__(self, metadata: Metadata, s3_client: boto3.client = None):
        self.metadata = metadata
        self.s3_client = s3_client

    def write(self, path: str, rows: int = None, desired_size: int = None, batch_size: int = 1000000,
              use_batches: bool = False, progress: bool = True, orient: str = None):
        """
        Generic entry point for the Writer.
        """
        if self.metadata.format == "csv":
            self._write_csv(path=path, rows=rows, desired_size=desired_size, batch_size=batch_size,
                            use_batches=use_batches, progress=progress)
        elif self.metadata.format == 'json':
            self._write_json(path=path, rows=rows, desired_size=desired_size, batch_size=batch_size,
                             use_batches=use_batches, progress=progress, orient=orient)
        else:
            raise NotImplementedError(f'Format {self.metadata.format} not implemented')

    def _write_csv(self, path: str, rows: int = None, desired_size: int = None, batch_size: int = 1000000,
                   use_batches: bool = False, progress: bool = True):
        """
        Entry point to write csv.
        """
        csv_writer = CSVWriter(metadata=self.metadata, path=path, s3_client=self.s3_client)
        csv_writer.write(rows=rows, progress=progress, batch_size=batch_size, use_batches=use_batches,
                         desired_size=desired_size)

    def _write_json(self, orient: str, path: str, rows: int = None, desired_size: int = None, batch_size: int = 1000000,
                    use_batches: bool = False, progress: bool = True):
        """
        Entry point to write JSON.
        """
        json_writer = JSONWriter(metadata=self.metadata, path=path, s3_client=self.s3_client)
        json_writer.write(rows=rows, progress=progress, batch_size=batch_size, use_batches=use_batches,
                          desired_size=desired_size, orient=orient)
