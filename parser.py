from parser_utils import regexes
from parser_utils.musician_page_object import MusicianPageObject

class WikiParser:
    def __init__(self):
        self.musician_flags = self.get_musician_flags('parser_utils/musician_occupancy_flags')
        self.musicians = []

    def parse(self, text):
        pages = regexes.SPLIT_PAGES.findall(text)
        self.musicians += self.filter_musicians(pages)
        self.write_musicians("data/musicians")

        # for page in pages:
        #     print(GenericPageObject(page))

    def get_musician_flags(self, flags_file_path):
        musician_flags = []
        with open(flags_file_path, 'r', encoding="utf8") as f:
            while (flag := f.readline().rstrip()):
                musician_flags.append(flag.lower())
        return musician_flags

    def write_musicians(self, musician_file_name):
        with open(musician_file_name, 'w', encoding="utf8") as f:
            for musician in self.musicians:
                f.write(str(musician))
            f.write("\n" + str(len(self.musicians)))

    def filter_musicians(self, pages):
        musicians = []
        for page in pages:
            occupations = regexes.PAGE_GET_OCCUPATION.findall(page)
            for occupation in occupations:
                if self.is_musician_page(occupation):
                    musicians.append(MusicianPageObject(page))

        return musicians

    def is_musician_page(self, occupation):
        return any(x in occupation.lower() for x in self.musician_flags)
