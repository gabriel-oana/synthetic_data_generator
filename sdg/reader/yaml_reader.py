import yaml
from sdg.reader.base_reader import BaseReader


class YAMLReader(BaseReader):

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
            try:
                yaml.add_constructor("!join", self.yaml_join)
                yaml_object = yaml.unsafe_load(stream)

                return yaml_object
            except yaml.YAMLError as exc:
                raise RuntimeError(f"{exc}")
