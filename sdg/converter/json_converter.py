import json

from sdg.builder.builder import Builder
from sdg.dto.metadata import Metadata
from sdg.dto.synthetic_data import SyntheticData


class JSONConverter:

    def __init__(self, metadata: Metadata):
        self.metadata = metadata

    def create(self, rows: int, orient: str = 'records', progress: bool = True, progress_message: str = None) -> str:
        """
        Creates the csv data as a string to be passed to a writer.
        """
        valid_orientations = ["split", "records"]
        if orient not in valid_orientations:
            raise ValueError("Incorrect orient. Valid choices: split, records")

        builder = Builder(metadata=self.metadata)
        vals = builder.build_dataset(rows=rows, progress=progress, progress_message=progress_message)
        if orient == "split":
            return json.dumps(vals.__dict__)
        else:
            return self._records_orient(vals)

    @staticmethod
    def _records_orient(values: SyntheticData):
        """
        Formats the json like [{column -> value}, ..., {column -> value}]
        """
        data = []
        for data_value in values.values:
            record = zip(values.columns, data_value)
            data.append(dict(record))
        return json.dumps(data)
