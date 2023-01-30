from sdg.utils.base_dump import BaseDump


class LocalDump(BaseDump):

    def write(self, path: str, body: str):
        """
        Writes a local csv file containing all data.
        """
        with open(path, "w", encoding='utf-8') as file:
            file.write(body)
