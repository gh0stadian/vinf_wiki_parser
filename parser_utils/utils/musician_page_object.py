import parser_utils.utils.regexes as regexes
from parser_utils.utils.infobox_object import InfoboxObject
from parser_utils.utils.discography_object import DiscographyObject
import json

class MusicianPageObject:
    def __init__(self, title, about, discography):
        self.title = title
        self.about = about
        self.discography = discography

    @classmethod
    def from_raw(cls, text):
        title = regexes.PAGE_GET_TITLE.search(text).group(1)
        if infobox := regexes.PAGE_GET_BOX.findall(text):
            infobox = InfoboxObject.from_raw(list(filter(regexes.PAGE_GET_INFOBOX.match, infobox))[0])
        else:
            infobox = InfoboxObject({})

        if discography := regexes.PAGE_GET_DISCOGRAPHY.search(text):
            discography = DiscographyObject.from_raw(discography.group(1))
        else:
            discography = DiscographyObject([])
        return MusicianPageObject(title, infobox, discography)

    @classmethod
    def from_json(cls, json_dump):
        object = json.loads(json_dump)
        title = object['title']
        about = InfoboxObject(object['about'])
        discography = DiscographyObject(object['songs'])
        return MusicianPageObject(title, about, discography)

    def to_json(self):
        return {"title": self.title, **self.about.__dict__, **self.discography.__dict__}

    def __str__(self):
        o = "=" * 80 + "\n"
        o += self.title + "\n"
        # if self.infobox:
        o += str(self.about) + "\n"
        if self.discography and self.discography.songs:
            o += str(self.discography) + "\n"
        return o
