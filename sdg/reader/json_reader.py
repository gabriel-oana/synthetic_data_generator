import json
from sdg.reader.base_reader import BaseReader


class JSONReader(BaseReader):

    def read(self, file: str):
        with open(file, "r", encoding='utf-8') as stream:
            metadata = json.loads(stream.read())

        return metadata
