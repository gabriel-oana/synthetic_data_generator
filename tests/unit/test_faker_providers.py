import unittest
from sdg.providers.faker_providers import IdProvider, ElementProvider
from sdg.providers.faker_factory import FakerFactory


class TestFakerProviders(unittest.TestCase):

    def test_id_provider_numeric_id(self):
        faker_factory = FakerFactory()
        faker_factory.register_provider(IdProvider)
        faker_instance = faker_factory()

        expected_answer = 12
        actual_answer = len(str(faker_instance.numeric_id(length=12)))
        self.assertEqual(expected_answer, actual_answer)

    def test_id_provider_string_id(self):
        faker_factory = FakerFactory()
        faker_factory.register_provider(IdProvider)
        faker_instance = faker_factory()

        expected_answer = 12
        actual_answer = len(str(faker_instance.string_id(length=12)))
        self.assertEqual(expected_answer, actual_answer)

    def test_element_choice_string_id(self):
        faker_factory = FakerFactory()
        faker_factory.register_provider(ElementProvider)
        faker_instance = faker_factory()

        expected_answer = 'B'
        actual_answer = faker_instance.choice(elements=["A", "B"], seed=1)
        self.assertEqual(expected_answer, actual_answer)