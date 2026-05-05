class DictionaryFileNotFound(FileNotFoundError):
    pass


class InvalidDictionaryFile(Exception):
    pass


class InvalidDictionaryFileContent(Exception):
    pass


class ArticleMissingKeyPhrase(Exception):
    pass


class MultipleDefinitionElements(Exception):
    pass
