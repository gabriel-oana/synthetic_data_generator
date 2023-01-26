from faker import Faker
from sdg.dto.metadata import Metadata


class Row:

    def build(self, metadata: Metadata) -> list:

        row_values = []
        if len(metadata.columns) == 0:
            raise ValueError("Columns are not set")

        for column in metadata.columns:
            if column.null_probability > 0:
                if self._should_be_null(null_probability=column.null_probability, faker=column.faker):
                    row_values.append(None)
                else:
                    value = column.faker_callable(**column.args)
                    row_values.append(value)

            else:
                value = column.faker_callable(**column.args)
                row_values.append(value)
        return row_values

    @staticmethod
    def _should_be_null(null_probability: float, faker: Faker):
        """
        The way to calculate this and provide reliability is by using the boolean functionality from Faker.
        Theoretically, one could use a random number generator and check if it's below a certain value,
        however, this method does not allow for setting a seed and "replaying" the same data.
        """
        return faker.boolean(chance_of_getting_true=round(null_probability * 100))
