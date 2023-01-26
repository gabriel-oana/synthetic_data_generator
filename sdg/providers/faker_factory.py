from faker import Faker
from sdg.providers.faker_providers import IdProvider, ElementProvider


class FakerFactory:

    def __init__(self, faker: Faker = None, locale: str = 'en-GB'):
        self._faker = faker
        self._locale = locale

    def __call__(self):
        self.faker = self._faker if self._faker else Faker([self._locale])
        self.register_providers()
        return self.faker

    def register_providers(self):
        self.faker.add_provider(IdProvider)
        self.faker.add_provider(ElementProvider)

    def register_provider(self, provider):
        self.faker.add_provider(provider)

