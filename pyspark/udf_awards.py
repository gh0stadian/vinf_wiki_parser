import re

from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def parse_awards(text):
    """Parses awards from text."""
    PAGE_GET_AWARDS = re.compile(r"== *?Awards and nominations *?==\n(.*?\n)==[\w\s]", flags=re.I | re.DOTALL)
    PAGE_GET_AWARDS2 = re.compile(r"== *?Awards *?==\n(.*?\n)==[\w\s]", flags=re.I | re.DOTALL)
    AWARDS_REPETITION = re.compile(r"\*\*\*(\d+)\*\*\*(.*)", re.DOTALL)
    AWARDS_CELL = re.compile(r"\|\s*(.*?)\n")
    AWARDS_ROWSPAN = re.compile(r"rowspan=.*?(\d+).*?\|\s*", re.DOTALL)
    AWARDS_HTML_TAG = re.compile(r"[\w]*?=[^\||\n]*\|\s*", re.DOTALL)
    AWARDS_HEADER_1 = header = re.compile(r"(\{\|.*?)\|\s*-", re.DOTALL)
    AWARDS_HEADER_2 = re.compile(r"^\{\{.*?\}\}\n\|-", re.DOTALL)
    AWARDS_NOMINATED_FLAG = re.compile(r"\{\{\s*nom[^}]*?\}\}", flags=re.I | re.DOTALL)
    AWARDS_WINNER_FLAG = re.compile(r"\{\{\s*won[^}]*?\}\}", flags=re.I | re.DOTALL)
    INFOBOX_LT_GT = re.compile(r"&lt.*?&gt;", re.DOTALL)
    
    def preprocess_awards(text):
        """Preprocesses the awards section of a page."""
        text = text.replace('&amp;', '&')
        text = text.replace('&ndash;', '-')
        text = text.replace('&quot;', '"')
        text = text.replace('\n!', '\n|')
        text = re.sub(INFOBOX_LT_GT, '', text)
        text = re.sub(AWARDS_NOMINATED_FLAG, "Nominated", text)
        text = re.sub(AWARDS_WINNER_FLAG, "Winner", text)
        text = text.replace("[[", '')
        text = text.replace("\n}}", '')
        text = text.replace("]]", '')
        text = AWARDS_ROWSPAN.sub("***\\1***", text)
        text = AWARDS_HTML_TAG.sub("", text)
        text = AWARDS_HEADER_1.sub("", text)
        text = AWARDS_HEADER_2.sub("", text)
        text = text.replace("\n|}", "")
        return text

    if awards := PAGE_GET_AWARDS.search(text):
        awards = awards.group(1)
    elif awards := PAGE_GET_AWARDS2.search(text):
        awards = awards.group(1)
    else:
        return "[]"

    awards = preprocess_awards(awards)
    split = awards.split("|-")
    if not split[0].startswith("\n|"):
        split = split[1:]
    awards_table = [AWARDS_CELL.findall(row) for row in split]
    for i, row in enumerate(awards_table):
        for j, element in enumerate(row):
            awards_table[i][j] = element.replace("\n", "")
            if repeat := AWARDS_REPETITION.search(element):
                awards_table[i][j] = repeat.group(2)
                for k in range(1, int(repeat.group(1))):
                    if i + k >= len(awards_table):
                        break
                    awards_table[i + k].insert(j, awards_table[i][j])

    return str(awards_table)