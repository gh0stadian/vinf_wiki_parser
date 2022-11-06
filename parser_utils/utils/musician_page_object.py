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
        title = regexes.PAGE_GET_TITLE.search(text).group(1)

        if infobox := regexes.PAGE_GET_INFOBOX.findall(text):
            infobox = InfoboxObject.from_raw(infobox[0])
        else:
            return None

        if discography := regexes.PAGE_GET_DISCOGRAPHY.search(text):
            discography = DiscographyObject.from_raw(discography.group(1))
        else:
            discography = DiscographyObject([])

        if awards := regexes.PAGE_GET_AWARDS.search(text):
            awards = AwardsObject.from_raw(awards.group(1))
        else:
            awards = AwardsObject([])

        return MusicianPageObject(title, infobox, discography, awards)

    @classmethod
    def from_json(cls, json_dump):
        object = json.loads(json_dump)
        title = object['title']
        about = InfoboxObject(object['about'])
        discography = DiscographyObject(object['songs'])
        return MusicianPageObject(title, about, discography)

    def to_json(self):
        return {"title": self.title, **self.about.__dict__, **self.discography.__dict__, **self.awards.__dict__}

    def __str__(self):
        o = "=" * 80 + "\n"
        o += self.title + "\n"
        o += str(self.about) + "\n"
        if self.discography and self.discography.songs:
            o += str(self.discography) + "\n"
        if self.awards and self.awards.awards_list:
            o += str(self.awards) + "\n"
        return o
