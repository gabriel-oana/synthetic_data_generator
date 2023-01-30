import yaml
from sdg.reader.base_reader import BaseReader


class YAMLReader(BaseReader):

    def read(self, file: str):
        with open(file, "r", encoding='utf-8') as stream:
            try:
                yaml_object = yaml.safe_load(stream)

                return yaml_object
            except yaml.YAMLError as exc:
                raise RuntimeError(f"{exc}")
