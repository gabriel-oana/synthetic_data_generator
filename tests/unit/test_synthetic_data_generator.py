import unittest


class TestSyntheticDataGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.metadata_path = 'tests/data_files/schema.yaml'

