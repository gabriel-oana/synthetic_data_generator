from alive_progress import alive_it

from sdg.dto.synthetic_data import SyntheticData
from sdg.dto.metadata import Metadata
from sdg.builder.row import Row


class Builder:

    def __init__(self, metadata: Metadata):
        self._metadata = metadata
        self._row = Row()

    def build_dataset(self, rows: int = None, progress: bool = None, progress_message: str = None) -> SyntheticData:
        """
        Builds the data from the metadata information and stores it in the SyntheticData DTO.
        """
        # Construct output and add all data in memory
        row_values = []

        if progress:
            row_range = alive_it(
                range(rows),
                dual_line=True,
                title="Generating data" if not progress_message else progress_message,
            )
        else:
            row_range = range(rows)

        for _ in row_range:
            row_values.append(self._row.build(metadata=self._metadata))

        synthetic_data = SyntheticData(
            columns=self._metadata.column_names,
            values=row_values
        )
        return synthetic_data
