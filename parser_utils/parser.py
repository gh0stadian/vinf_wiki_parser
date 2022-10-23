import json
import os

from parser_utils.utils import regexes
from parser_utils.utils.musician_page_object import MusicianPageObject


class WikiParser:
    def __init__(self, output_file):
        self.musician_flags = self.get_musician_flags('parser_utils/utils/musician_occupancy_flags')
        self.output_file = output_file
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def parse(self, text):
        pages = regexes.SPLIT_PAGES.findall(text)
        musicians = self.filter_musicians(pages)
        if musicians:
            self.write_musicians(musicians)

    def get_musician_flags(self, flags_file_path):
        musician_flags = []
        with open(flags_file_path, 'r', encoding="utf8") as f:
            while flag := f.readline().rstrip():
                musician_flags.append(flag.lower())
        return musician_flags

    def write_musicians(self, musicians):
        with open(self.output_file, 'a', encoding="utf8") as f:
            for musician in musicians:
                json.dump(musician.to_json(), f)
                f.write("\n")
                # f.write(str(musician.to_json()) + "\n")

    def filter_musicians(self, pages):
        musicians = []
        for page in pages:
            occupations = regexes.PAGE_GET_OCCUPATION.findall(page)
            for occupation in occupations:
                if self.is_musician_page(occupation):
                    musicians.append(MusicianPageObject.from_raw(page))

        return musicians

    def is_musician_page(self, occupation):
        return any(x in occupation.lower() for x in self.musician_flags)
