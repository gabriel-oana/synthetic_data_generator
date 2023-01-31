import os
import glob
import unittest
import boto3
import moto
from sdg import SDG
from sdg.dto.metadata import Metadata, Column


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

    def test_raises_with_no_columns(self):
        metadata = Metadata(
            columns=[],
            file_name='test',
            format='csv'
        )

        sdg = SDG(metadata=metadata)
        self.assertRaises(ValueError, sdg.json_sample)

    def test_write_json(self):
        column1 = Column(
            name='col1',
            type='string',
            unique=False,
            seed=1
        )

        column2 = Column(
            name='col2',
            type='random_element',
            args={
                "elements": ["A", "B", "C"]
            },
            seed=1,
            super_seed=1
        )

        metadata = Metadata(
            columns=[column1, column2],
            file_name='test',
            format='json',
        )

        sdg = SDG(metadata=metadata)
        sample = sdg.json_sample(rows=1, progress=True)

        expected_string = '{"columns": ["col1", "col2"], "values": [["gSNnzxHPebRwNaxLlXUb", "A"]]}'
        self.assertEqual(sample, expected_string)

    def test_write_json_raises_with_wrong_orientation(self):
        column1 = Column(
            name='col1',
            type='string',
            unique=False,
            seed=1
        )

        column2 = Column(
            name='col2',
            type='random_element',
            args={
                "elements": ["A", "B", "C"]
            },
            seed=1,
            super_seed=1
        )

        metadata = Metadata(
            columns=[column1, column2],
            file_name='test',
            format='json',
        )

        sdg = SDG(metadata=metadata)
        self.assertRaises(ValueError, sdg.json_sample, orient="WRONG-CHOICE")

    def test_write_json_with_orient_records(self):
        column1 = Column(
            name='col1',
            type='string',
            unique=True,
            seed=1
        )

        column2 = Column(
            name='col2',
            type='random_element',
            args={
                "elements": ["A", "B", "C"]
            },
            seed=1,
            super_seed=1
        )

        metadata = Metadata(
            columns=[column1, column2],
            file_name='test',
            format='json',
        )

        sdg = SDG(metadata=metadata)
        sample = sdg.json_sample(rows=1, progress=True, orient='records')

        expected_string = '[{"col1": "gSNnzxHPebRwNaxLlXUb", "col2": "A"}]'
        self.assertEqual(sample, expected_string)

    @moto.mock_s3
    def test_write_csv_to_s3(self):
        s3_client = boto3.client("s3", region_name="eu-west-1")
        s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-1"})

        sdg = SDG(metadata=self.metadata, s3_client=s3_client)
        sdg.write(
            path="s3://test-bucket/test.csv",
            rows=10,
            use_batches=False
        )

        objects = s3_client.list_objects_v2(Bucket='test-bucket')
        number_of_files = len(objects['Contents'])

        self.assertEqual(number_of_files, 1)

    @moto.mock_s3
    def test_write_csv_to_s3_in_batch(self):
        s3_client = boto3.client("s3", region_name="eu-west-1")
        s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-1"})

        sdg = SDG(metadata=self.metadata, s3_client=s3_client)
        sdg.write(
            path="s3://test-bucket/test.csv",
            rows=10,
            batch_size=5,
            use_batches=True
        )

        objects = s3_client.list_objects_v2(Bucket='test-bucket')
        number_of_files = len(objects['Contents'])

        self.assertEqual(number_of_files, 2)

    @moto.mock_s3
    def test_write_csv_to_s3_in_one_batch(self):
        s3_client = boto3.client("s3", region_name="eu-west-1")
        s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-1"})

        sdg = SDG(metadata=self.metadata, s3_client=s3_client)
        sdg.write(
            path="s3://test-bucket/test.csv",
            rows=10,
            batch_size=100,
            use_batches=True
        )

        objects = s3_client.list_objects_v2(Bucket='test-bucket')
        number_of_files = len(objects['Contents'])

        self.assertEqual(number_of_files, 1)

    @moto.mock_s3
    def test_write_json_to_s3(self):
        s3_client = boto3.client("s3", region_name="eu-west-1")
        s3_client.create_bucket(Bucket="test-bucket", CreateBucketConfiguration={"LocationConstraint": "eu-west-1"})

        column1 = Column(
            name='col1',
            type='string',
            unique=True,
            seed=1
        )

        metadata = Metadata(
            columns=[column1],
            file_name='test',
            format='json',
        )

        sdg = SDG(metadata=metadata, s3_client=s3_client)
        sdg.write(rows=1, progress=True, json_orient='records', path="s3://test-bucket/test.json")

        objects = s3_client.list_objects_v2(Bucket='test-bucket')
        number_of_files = len(objects['Contents'])

        self.assertEqual(number_of_files, 1)
