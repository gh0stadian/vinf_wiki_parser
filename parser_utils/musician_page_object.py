import parser_utils.regexes as regexes
from parser_utils.generic_page_object import GenericPageObject
from parser_utils.infobox_object import InfoboxObject


class MusicianPageObject(GenericPageObject):
    def __init__(self, text):
        super().__init__(text)

    def _parse(self, text):
        self.title = regexes.PAGE_GET_TITLE.search(text).group(1)
        infobox = regexes.PAGE_GET_INFOBOX.search(text)
        if infobox is not None:
            self.infobox = InfoboxObject(regexes.PAGE_GET_INFOBOX.search(text).group())

    def __str__(self):
        o = "=" * 80 + "\n"
        o += self.title + "\n"
        o += str(self.infobox) + "\n"
        return o + "=" * 80
