import os
import time
import shutil
import warnings
from pathlib import Path
import boto3

from sdg.dto.metadata import Metadata
from sdg.utils.s3_dump import S3Dump
from sdg.utils.local_dump import LocalDump
from sdg.converter.json_converter import JSONConverter
from sdg.utils.seq import split_sequence


class JSONWriter:

    def __init__(self, metadata: Metadata, path: str, s3_client: boto3.client = None):
        self.metadata = metadata
        self.path = path
        self.s3_client = s3_client
        self.json_converter = JSONConverter(metadata=metadata)

        if "s3://" in path:
            self.dumper = S3Dump(s3_client=self.s3_client)
        else:
            self.dumper = LocalDump()

    def write(self, rows: int = None, desired_size: int = None, batch_size: int = 1000000, use_batches: bool = False,
              progress: bool = True, orient: str = 'split') -> None:
        """
        Entry point for writing data in any combination.
        """
        self.validate(desired_size=desired_size, rows=rows, use_batches=use_batches)
        rows_required = self._estimate_rows_from_size(desired_size=desired_size, progress=progress) if desired_size else rows

        if use_batches:
            batch_range = self._make_batch_list(rows=rows_required, batch=batch_size)
            self._write_in_batches(path=self.path, batch_range=batch_range, progress=progress, rows=rows_required, orient=orient)
        else:
            self._write_one_set(path=self.path, rows=rows_required, progress=progress, orient=orient)

    def _write_one_set(self, path: str, rows: int, progress: bool, orient: str) -> None:
        """
        Writes a local csv file containing all data.
        """
        csv_data = self.json_converter.create(rows=rows, progress=progress, orient=orient)
        self.dumper.write(path=f"{path}/{self.metadata.file_name}.json", body=csv_data)

    def _write_in_batches(self, path: str, rows: int, batch_range: list, progress: bool, orient: str) -> None:
        """
        Writes the output in batches and writes them to disk.
        """

        file_counter = 0
        row_counter = 0
        for batch in batch_range:
            file_counter += 1
            row_counter += batch
            file_name = f"{self.metadata.file_name}-part_{file_counter}.json"
            progress_msg = f"Creating part {file_counter} / {len(batch_range)} ({row_counter}/{rows})"

            csv_data = self.json_converter.create(rows=batch, progress=progress, progress_message=progress_msg, orient=orient)
            self.dumper.write(path=f"{path}/{file_name}", body=csv_data)

    @staticmethod
    def _make_batch_list(batch: int, rows: int) -> list:
        """
        Creates a list of batches to be processed.
        For example, if the number of rows required is 1340 and the batch size is 1000 then
        the output like this: [1000, 340]
        """

        if rows > batch:
            batch_range = split_sequence(rows, batch)
        else:
            batch_range = [rows]

        return batch_range

    def _estimate_rows_from_size(self, desired_size: float, sample_row_size: int = 100000, progress: bool = False):
        """
        Makes an estimate on the number of rows based on the size required.
        It creates a file of a sample size, it measures the size of it then it deletes it and infers the number of rows
        required.
        """

        temp_path = f'{os.path.abspath("")}/tmp'
        temp_file = f'{temp_path}/{self.metadata.file_name}.csv'

        # Check if the path exists otherwise create it.
        if not os.path.exists(temp_path):
            Path(temp_path).mkdir(parents=True, exist_ok=True)

        # Create the file
        csv_data = self.json_converter.create(rows=sample_row_size, progress=progress,
                                              progress_message="Estimating number of rows required")
        self.dumper.write(path=temp_file, body=csv_data)

        # Get size of the file
        avg_size_per_row = (os.path.getsize(temp_file) / 1048576) / sample_row_size

        # Remove the tmp file
        time.sleep(0.5)
        if os.path.exists(temp_path):
            shutil.rmtree(temp_path)

        rows_required = int(desired_size / avg_size_per_row)
        if progress:
            print(f"Rows required to generate {desired_size} MB of data: {rows_required}")

        return rows_required

    @staticmethod
    def validate(desired_size: int = None, rows: int = None, use_batches: bool = None):
        """
        Validates if the number of rows or desired size is too big to be computed locally.
        It will display a warning only.
        """
        if desired_size and not use_batches:
            if desired_size >= 1024:
                warnings.warn("Dataset might not fit in memory. Consider using batching")

        if rows and not use_batches:
            if rows >= 100000000:
                warnings.warn("Dataset might not fit in memory. Consider using batching")
