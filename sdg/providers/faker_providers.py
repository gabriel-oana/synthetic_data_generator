import random
from typing import Any
from faker.providers import BaseProvider


class IdProvider(BaseProvider):

    def numeric_id(self, length: int = 12) -> int:
        return self.random_number(digits=length, fix_len=True)

    def string_id(self, length: int = 8) -> str:
        return ''.join(self.random_letters(length=length))


class ElementProvider(BaseProvider):

    @staticmethod
    def choice(elements: list, seed: int = None) -> Any:
        """
        Implementation of random element with seed enabled.
        If the seed is enabled, then the sequence can be repeated in the same order.
        """
        if seed:
            random.seed(seed)
            random.shuffle(elements)
            random.getstate()

        return random.choice(elements)
