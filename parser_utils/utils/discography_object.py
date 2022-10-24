import re


class DiscographyObject():
    def __init__(self, songs):
        self.songs = songs

    @classmethod
    def from_raw(cls, raw_discography):
        # categories = raw_discography.split("===")
        regex = re.compile(r"''\[*(.*?)\]*''")
        albums = list(set(regex.findall(raw_discography)))
        return DiscographyObject(albums)

    def __str__(self):
        o = "Discography".ljust(80, "-") + "\n"
        for single in self.songs:
            o += " " * 5 + f"{single}\n"
        return o
