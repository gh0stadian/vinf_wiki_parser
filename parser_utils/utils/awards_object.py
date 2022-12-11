import re
import parser_utils.utils.regexes as regexes

from parser_utils.utils.utils import remove_html_rowspan, preprocess_awards, remove_header_footer


class AwardsObject():
    def __init__(self, awards):
        self.awards_list = awards

    @classmethod
    def from_raw(cls, raw_awards):
        """Creates an AwardsObject from a raw awards string."""
        awards = preprocess_awards(raw_awards)
        awards = remove_html_rowspan(awards)
        awards = remove_header_footer(awards)

        split = awards.split("|-")
        if not split[0].startswith("\n|"):
            split = split[1:]

        awards_table = [regexes.AWARDS_CELL.findall(row) for row in split]
        for i, row in enumerate(awards_table):
            for j, element in enumerate(row):
                awards_table[i][j] = element.replace("\n", "")
                if repeat := regexes.AWARDS_REPETITION.search(element):
                    awards_table[i][j] = repeat.group(2)
                    for k in range(1, int(repeat.group(1))):
                        awards_table[i + k].insert(j, awards_table[i][j])
        return AwardsObject(awards_table)

    def __str__(self):
        """Returns a string representation of the object."""
        o = "Awards".ljust(80, "-") + "\n"
        for row in self.awards_list:
            for element in row:
                o += element[:30].ljust(30, " ") + "|"
            o += "\n"
        return o
