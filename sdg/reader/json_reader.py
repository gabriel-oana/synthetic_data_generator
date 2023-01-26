import json
from sdg.reader.base_reader import BaseReader


class JSONReader(BaseReader):

    @staticmethod
    def yaml_join(loader, node) -> str:
        """
        Handler to join strings within a yaml file.
        !join [a,b,c]
        """
        seq = loader.construct_sequence(node)
        return ''.join([str(i) for i in seq])

    def read(self, file: str):
        with open(file, "r") as stream:
            metadata = json.loads(stream.read())

        return metadata