from typing import Union, Dict, Optional

from sdg.reader.yaml_reader import YAMLReader
from sdg.reader.json_reader import JSONReader
from sdg.dto.metadata import Metadata


class Reader:

    @staticmethod
    def import_metadata(metadata: Optional[Union[Dict, Metadata]] = None) -> Metadata:
        """
        Imports a file and converts it to a metadata object.
        It accepts the metadata object directly.
        It accepts the metadata as a dict as well.
        """
        if isinstance(metadata, str):
            file_type = metadata.split('.')[-1]
            if file_type.lower() in ["yaml", "yml"]:
                reader = YAMLReader()
            elif file_type.lower() == "json":
                reader = JSONReader()
            else:
                raise RuntimeError(f"File type {file_type} not recognised")
            content = reader.read(metadata)

        elif isinstance(metadata, Metadata):
            content = metadata.__dict__

        elif isinstance(metadata, dict):
            content = metadata

        else:
            raise RuntimeError(f"Metadata {metadata} not recognised")

        meta = Metadata(**content)
        return meta
