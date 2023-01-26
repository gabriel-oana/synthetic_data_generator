import time
from typing import List
from alive_progress import alive_it
from prettytable import PrettyTable

from sdg.synthetic_data_generator import SDG
from sdg.dto.metadata import Column, Metadata


def lap_time(f):
    """
    This wrapper measures the time taken for a specific function
    """
    def wrap(*args, **kwargs):
        ts = time.time()
        column_name, unique, null_prob = f(*args, **kwargs)
        te = time.time()

        time_taken = round((te-ts), 3)
        return column_name, unique, null_prob, time_taken
    return wrap


class Performance:

    def __init__(self, iterations: int = 100000, progress: bool = True):
        self.iterations = iterations
        self.progress = progress

    def __call__(self):
        results = []
        for case in self.test_cases():
            results.append(self.measure(case))

        # Make tables
        t = PrettyTable(['Provider', 'Unique Records', 'Null Probability',  f"Δs ({self.iterations} records)"])
        for row in results:
            t.add_row(row)
        t.align["Provider"] = 'l'
        print(t)

    @lap_time
    def measure(self, column: Column):
        """
        Measures the performance of one column at a time.
        """
        metadata = Metadata(
            file_name='performance-test',
            format='csv',
            separator=',',
            columns=[column]
        )
        sdg = SDG(metadata=metadata)

        if self.progress:
            row_range = alive_it(range(self.iterations), dual_line=True, title=f'---> {column.name}')
        else:
            row_range = range(self.iterations)

        vals = []
        for _ in row_range:
            vals.append(sdg.csv_sample(rows=1))

        return column.name, column.unique, column.null_probability

    @staticmethod
    def test_cases() -> List[Column]:
        cases = [
            {"name": "Element Choice", "type": "random_element", "null_probability": 0.3, "seed": 1, "args": {"elements": ["A", "B", "C"]}},
            {"name": "Element Choice", "type": "random_element", "null_probability": 0, "seed": 1, "args": {"elements": ["A", "B", "C"]}},
            {"name": "Numeric ID", "type": "numeric_id", "null_probability": 0, "seed": 1, "unique": False, "args": {"length": 12}},
            {"name": "Numeric ID", "type": "numeric_id", "null_probability": 0, "seed": 1, "unique": True, "args": {"length": 12}},
            {"name": "Numeric ID", "type": "numeric_id", "null_probability": 0.3, "seed": 1, "unique": False, "args": {"length": 12}},
            {"name": "Numeric ID", "type": "numeric_id", "null_probability": 0.3, "seed": 1, "unique": True, "args": {"length": 12}},
            {"name": "String ID", "type": "string_id", "null_probability": 0, "seed": 1, "unique": False, "args": {"length": 12}},
            {"name": "String ID", "type": "string_id", "null_probability": 0, "seed": 1, "unique": True, "args": {"length": 12}},
            {"name": "String ID", "type": "string_id", "null_probability": 0.3, "seed": 1, "unique": False, "args": {"length": 12}},
            {"name": "String ID", "type": "string_id", "null_probability": 0.3, "seed": 1, "unique": True, "args": {"length": 12}},
            {"name": "String", "type": "string", "null_probability": 0, "seed": 1, "unique": False, "args": {"min_chars": 12, "max_chars": 24}},
            {"name": "String", "type": "string", "null_probability": 0, "seed": 1, "unique": True, "args": {"min_chars": 12, "max_chars": 24}},
            {"name": "String", "type": "string", "null_probability": 0.3, "seed": 1, "unique": False, "args": {"min_chars": 12, "max_chars": 24}},
            {"name": "String", "type": "string", "null_probability": 0.3, "seed": 1, "unique": True, "args": {"min_chars": 12, "max_chars": 24}},
            {"name": "Integer", "type": "integer", "null_probability": 0, "seed": 1, "unique": False, "args": {"min_value": -10000000, "max_value": 10000000}},
            {"name": "Integer", "type": "integer", "null_probability": 0, "seed": 1, "unique": True, "args": {"min_value": -10000000, "max_value": 10000000}},
            {"name": "Integer", "type": "integer", "null_probability": 0.3, "seed": 1, "unique": False, "args": {"min_value": -10000000, "max_value": 10000000}},
            {"name": "Integer", "type": "integer", "null_probability": 0.3, "seed": 1, "unique": True, "args": {"min_value": -10000000, "max_value": 10000000}},
            {"name": "Boolean", "type": "boolean", "null_probability": 0, "seed": 1, "unique": False},
            {"name": "Boolean", "type": "boolean", "null_probability": 0.3, "seed": 1, "unique": False},
            {"name": "Date", "type": "date", "null_probability": 0, "seed": 1, "unique": False, "args": {"pattern": "&Y-&m-&d"}},
            {"name": "Date", "type": "date", "null_probability": 0.3, "seed": 1, "unique": False, "args": {"pattern": "&Y-&m-&d"}},
            {"name": "Datetime", "type": "date", "null_probability": 0, "seed": 1, "unique": False, "args": {"pattern": "&Y-&m-&d %H:%M:%S"}},
            {"name": "Datetime", "type": "date", "null_probability": 0.3, "seed": 1, "unique": False, "args": {"pattern": "&Y-&m-&d %H:%M:%S"}},
            {"name": "String - Address", "type": "address", "null_probability": 0.3, "seed": 1, "unique": True},
            {"name": "String - Phone Number", "type": "phone_number", "null_probability": 0.3, "seed": 1, "unique": False},
        ]

        columns = []
        for case in cases:
            columns.append(Column(**case))

        return columns


if __name__ == '__main__':
    p = Performance(iterations=1000000)
    p()
