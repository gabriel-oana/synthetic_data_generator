import os
import glob
import unittest
from sdg import SDG


class TestSyntheticDataGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.metadata = 'tests/data_files/schema.yaml'

    def test_csv_sample(self):
        sdg = SDG(metadata=self.metadata)
        csv_sample = sdg.csv_sample(rows=2, progress=True)

        expected_string = """column_1,column_2,column_3,column_4,column_5,column_6
        SsUKNrClCWsfsld,B,76778227,18,2003-11-10 08:07:12,2003-11-10
        ZUweWdFrJRarP,C,45725232,752,1988-02-11 18:48:38,1988-02-11
        """
        self.assertEqual(csv_sample.replace('\r\n', ''), expected_string.strip().replace('  ', '').replace('\n', ''))

    def test_json_sample(self):
        sdg = SDG(metadata=self.metadata)
        json_sample = sdg.json_sample(rows=2)

        expected_string = """{"columns": ["column_1", "column_2", "column_3", "column_4", "column_5", "column_6"], "values": [["SsUKNrClCWsfsld", "B", 76778227, 18, "2003-11-10 08:07:12", "2003-11-10"], ["ZUweWdFrJRarP", "C", 45725232, 752, "1988-02-11 18:48:38", "1988-02-11"]]}"""
        self.assertEqual(json_sample, expected_string)

    def test_write_csv(self):
        sdg = SDG(metadata=self.metadata)
        sdg.write(
            path='.',
            rows=2,
            progress=True,
        )

        files = glob.glob('*.csv')
        files_length = len(files)

        for file in files:
            os.remove(file)

        self.assertEqual(files_length, 1)

    def test_write_csv_in_batches(self):
        sdg = SDG(metadata=self.metadata)
        sdg.write(
            path='.',
            rows=2,
            progress=True,
            use_batches=True,
            batch_size=1
        )

        files = glob.glob('*.csv')
        files_length = len(files)

        for file in files:
            os.remove(file)

        self.assertEqual(files_length, 2)

    def test_write_csv_with_desired_size(self):
        sdg = SDG(metadata=self.metadata)
        sdg.write(
            path='.',
            desired_size=1,
            progress=True,
            use_batches=True,
            batch_size=10000
        )

        files = glob.glob('*.csv')
        files_length = len(files)

        for file in files:
            os.remove(file)

        self.assertEqual(files_length, 2)