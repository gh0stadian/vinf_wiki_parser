import parser_utils.utils.regexes as regexes
from parser_utils.utils.infobox_object import InfoboxObject
from parser_utils.utils.discography_object import DiscographyObject
from parser_utils.utils.awards_object import AwardsObject
import json


class MusicianPageObject:
    def __init__(self, title, about, discography, awards):
        self.title = title
        self.about = about
        self.discography = discography
        self.awards = awards

    @classmethod
    def from_raw(cls, text):
        """Creates a MusicianPageObject from a raw wiki page text."""
        title = regexes.PAGE_GET_TITLE.search(text).group(1)

        # Get the infobox
        if infobox := regexes.PAGE_GET_INFOBOX.findall(text):
            infobox = InfoboxObject.from_raw(infobox[0])
        else:
            return None

        # Get the discography
        if discography := regexes.PAGE_GET_DISCOGRAPHY.search(text):
            discography = DiscographyObject.from_raw(discography.group(1))
        else:
            discography = DiscographyObject([])

        # Get the awards
        if awards := regexes.PAGE_GET_AWARDS.search(text):
            awards = AwardsObject.from_raw(awards.group(1))
        elif awards := regexes.PAGE_GET_AWARDS2.search(text):
            awards = AwardsObject.from_raw(awards.group(1))
        else:
            awards = AwardsObject([])

        return MusicianPageObject(title, infobox, discography, awards)

    @classmethod
    def from_json(cls, json_dump):
        """Creates a MusicianPageObject from a json dump."""
        object = json.loads(json_dump)
        title = object['title']
        about = InfoboxObject(eval(object['about']))
        discography = DiscographyObject(eval(object['songs']))
        awards = AwardsObject(eval(object['awards_list']))
        return MusicianPageObject(title, about, discography, awards)

    @classmethod
    def from_json_sn(cls, json_dump):
        """Creates a MusicianPageObject from a json dump."""
        object = json.loads(json_dump)
        title = object['title']
        about = InfoboxObject(object['about'])
        discography = DiscographyObject(object['songs'])
        awards = AwardsObject(object['awards_list'])
        return MusicianPageObject(title, about, discography, awards)

    def to_json(self):
        """Returns a json dump of the object."""
        return {"title": self.title, **self.about.__dict__, **self.discography.__dict__, **self.awards.__dict__}

    def __str__(self):
        """Returns a string representation of the object."""
        o = "=" * 80 + "\n"
        o += self.title + "\n"
        o += str(self.about) + "\n"
        if self.discography and self.discography.songs:
            o += str(self.discography) + "\n"
        if self.awards and self.awards.awards_list:
            o += str(self.awards) + "\n"
        return o
