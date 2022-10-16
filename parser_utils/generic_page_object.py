from abc import ABC


class GenericPageObject(ABC):
    def __init__(self, text):
        self.parsed = self._parse(text)

    def _parse(self, text):
        pass

    def __str__(self):
        pass
