import re

from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def parse_discography(text):
    """Parses discography from text."""
    PAGE_GET_DISCOGRAPHY = re.compile(r"== *?Discography *==\n(.*?\n)==[\w\s]", flags=re.I | re.DOTALL)
    DISCOGRAPHY_SUBCATEGORIES = re.compile(r"(?:'''|===) *?(.*?) *?(?:'''|===)\n(?:(.*?)\n\n|\{\|(.*?)\n\|\}\n)",
                                       flags=re.I | re.DOTALL
                                       )
    DISCOGRAPHY_SONGS = re.compile(r"''\[*(.*?)\]*''")
    

    discography = []
    raw_discography = PAGE_GET_DISCOGRAPHY.search(text)
    if not raw_discography:
        return "[]"
    else:
        raw_discography = raw_discography.group(1)
        
    
    discography_subcategories = DISCOGRAPHY_SUBCATEGORIES.findall(raw_discography)
    if not discography_subcategories:
        discography = list(set(DISCOGRAPHY_SONGS.findall(raw_discography)))
    for subtitle, body, _ in discography_subcategories:
        songs_in_body = list(set(DISCOGRAPHY_SONGS.findall(body)))
        subtitle = subtitle.replace("=", "").replace("[[", "").replace("]]", "")
        if songs_in_body:
            discography.append((subtitle.replace("=", ""), songs_in_body))
    
    return str(discography)