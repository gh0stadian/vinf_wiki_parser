import re
import parser_utils.utils.regexes as regexes


class DiscographyObject():
    def __init__(self, songs):
        self.songs = songs

    @classmethod
    def from_raw(cls, raw_discography):
        """Creates a DiscographyObject from a raw discography string."""
        discography = []
        discography_subcategories = regexes.DISCOGRAPHY_SUBCATEGORIES.findall(raw_discography)
        if not discography_subcategories:
            discography = list(set(regexes.DISCOGRAPHY_SONGS.findall(raw_discography)))
        for subtitle, body, _ in discography_subcategories:
            songs_in_body = list(set(regexes.DISCOGRAPHY_SONGS.findall(body)))
            subtitle = subtitle.replace("=", "").replace("[[", "").replace("]]", "")
            if songs_in_body:
                discography.append((subtitle.replace("=", ""), songs_in_body))
        return DiscographyObject(discography)

    def __str__(self):
        """Returns a string representation of the DiscographyObject."""
        o = "Discography".ljust(80, "-") + "\n"
        for item in self.songs:
            if isinstance(item, tuple):
                o += " " * 5 + f"{item[0]}\n"
                for songs in item[1]:
                    o += " " * 10 + f"{songs}\n"
            else:
                o += " " * 5 + f"{item}\n"
        return o
