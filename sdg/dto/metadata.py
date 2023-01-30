from typing import List, Optional
from dataclasses import dataclass
from sdg.providers.faker_factory import Faker, FakerFactory


def lookup_type(column_type: str) -> str:
    lookup_table = {
        "string": "pystr",
        "int": "pyint",
        "integer": "pyint",
        "float": "pyfloat",
        "bool": "boolean"
    }

    return lookup_table[column_type] if column_type in lookup_table.keys() else column_type


@dataclass
class Column:
    name: str
    type: str
    null_probability: Optional[float] = 0
    unique: Optional[bool] = False
    seed: Optional[int] = None
    locale: Optional[str] = None
    args: Optional[dict] = None
    super_seed: Optional[int] = None
    faker: Faker = None
    faker_callable: callable = None

    def __post_init__(self):

        if not self.args:
            self.args = {}

        # Set up Faker
        if not self.faker:
            faker_factory = FakerFactory(locale=self.locale if self.locale else 'en-GB')
            self.faker = faker_factory()

        # Apply seed
        if self.seed:
            self.faker.seed_instance(self.seed)

        if self.super_seed:
            self.faker.seed_instance(self.super_seed)

        # Convert the type when necessary
        self.type = lookup_type(self.type)

        # Create the callable
        if self.unique:
            self.faker_callable = getattr(self.faker.unique, self.type)
        else:
            self.faker_callable = getattr(self.faker, self.type)

        # Validate the args
        if self.faker_callable:
            faker_callable_expected_args = self.faker_callable.__code__.co_varnames
            for arg in list(self.args.keys()):
                if arg not in faker_callable_expected_args and "kwargs" not in faker_callable_expected_args:
                    raise RuntimeError(f"Argument '{arg}' not compatible with type {self.type}. \n"
                                       f"Valid choices: {faker_callable_expected_args}. \n"
                                       f"Check your metadata arguments for column {self.name}")


@dataclass
class Metadata:
    file_name: str
    format: str
    columns: List[Column]
    seed: Optional[int] = None
    separator: Optional[str] = ','
    column_names: List[str] = None

    def __post_init__(self):

        # Validate format
        allowed_formats = ["csv", "json"]
        if self.format.lower() not in allowed_formats:
            raise NotImplementedError(f'Format {self.format} not implemented. Allowed formats: {allowed_formats}')

        # Set up the columns
        columns = []
        for column in self.columns:
            if isinstance(column, Column):
                columns.append(column)
            else:
                columns.append(Column(**column, super_seed=self.seed))
        self.columns = columns

        # Set up column names
        self.column_names = [column.name for column in self.columns]
