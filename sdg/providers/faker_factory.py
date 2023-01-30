from faker import Faker
from sdg.providers.faker_providers import IdProvider, ElementProvider


class FakerFactory:

    def __init__(self, faker: Faker = None, locale: str = 'en-GB'):
        self._faker = faker if faker else Faker([locale])

    def __call__(self):
        self.register_providers()
        return self._faker

    def register_providers(self):
        self._faker.add_provider(IdProvider)
        self._faker.add_provider(ElementProvider)

    def register_provider(self, provider):
        self._faker.add_provider(provider)
