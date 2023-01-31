import unittest
from faker.providers import BaseProvider
from sdg.providers.faker_factory import FakerFactory


class TestProvider(BaseProvider):

    def test_func(self):
        return "test_case"


class TestFakerFactory(unittest.TestCase):

    def test_register_provider(self):
        faker_factory = FakerFactory()
        faker_factory.register_provider(TestProvider)
        faker_instance = faker_factory()

        expected_answer = 'test_case'
        actual_answer = faker_instance.test_func()
        self.assertEqual(expected_answer, actual_answer)