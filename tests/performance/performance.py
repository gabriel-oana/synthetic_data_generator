import os
import sys
import time
import json
import argparse
from typing import List
from pathlib import Path
from alive_progress import alive_it
from prettytable import PrettyTable

from sdg import SDG
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

    def __init__(self, iterations: int = 100000, progress: bool = True, show_table: bool = True):
        self.iterations = iterations
        self.progress = progress
        self.reports_path = 'reports/performance'
        self.file_name = 'performance'
        self.show_table = show_table

    def __call__(self):
        results = []
        for case in self.test_cases():
            results.append(self.measure(case))

        # Make tables
        t = PrettyTable(['Provider', 'Unique Records', 'Null Probability',  f"Δs ({self.iterations} records)"])
        for row in results:
            t.add_row(row)
        t.align["Provider"] = 'l'
        if self.show_table:
            print(t)

        # Compile results
        self.compile_results(results=results)

    def compile_results(self, results: list):
        """
        Compiles all the results into a report
        """
        # Create reports path if not exists
        temp_path = f'{os.path.abspath("")}/{self.reports_path}'
        if not os.path.exists(temp_path):
            Path(temp_path).mkdir(parents=True, exist_ok=True)

        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        file_results = {
            "python": python_version,
            "data": []
        }
        for result in results:
            file_results['data'].append({
                "provider": result[0],
                "unique_records": result[1],
                "null_probability": result[2],
                "time_sec": result[3]
            })

        with open(f"{temp_path}/{self.file_name}_{python_version}.json", 'w+') as f:
            f.write(json.dumps(file_results))

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
    parser = argparse.ArgumentParser(prog='Performance Test')
    parser.add_argument('-i', '--iterations', default=10000, type=int)
    parser.add_argument('-p', '--progress', default=False, type=bool)
    parser.add_argument('-t', '--show_table', default=False, type=bool)
    args = parser.parse_args()

    p = Performance(iterations=args.iterations, progress=args.progress, show_table=args.show_table)
    p()
