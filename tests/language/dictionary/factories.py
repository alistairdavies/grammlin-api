import factory

from language.dictionary.models import DictionaryEntry


class DictionaryEntryFactory(factory.Factory):
    class Meta:
        model = DictionaryEntry

    headword = factory.Faker("word")
    part_of_speech = "noun"
    translations = factory.LazyFunction(lambda: [])
    definition = factory.Faker("sentence")
    conjunction_parts = None
