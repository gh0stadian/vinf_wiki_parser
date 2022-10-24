import re

# DOCUMENT REGEXES
SPLIT_PAGES = re.compile(r"<page>(.*?)</page>", re.DOTALL)

# PAGE REGEXES
PAGE_GET_TITLE = re.compile(r"<title>(.*?)</title>", re.DOTALL)
PAGE_GET_OCCUPATION = re.compile(r"\| occupation *?= ({{.*?}}|.*?\n)", re.DOTALL)
PAGE_GET_INFOBOX = re.compile(r"\{\{Infobox(?:(?:\{\{(?:(?:\{\{(?:[^{}])*\}\})|(?:[^{}]))*\}\})|(?:[^{}]))*\}\}",
                              flags=re.I | re.DOTALL)
PAGE_GET_DISCOGRAPHY = re.compile(r"== *?Discography *==\n(.*?)\n==\w", re.DOTALL)

# INFOBOX REGEXES
INFOBOX_VAR_VAL = re.compile(r"(\S*)\s*=\s*(.*)", re.DOTALL)
INFOBOX_BIRTH_YMD = re.compile(r"\{\{birth.*(\d\d\d\d)\| *(\d+)\| *(\d+)", flags=re.I | re.DOTALL)
INFOBOX_BIRTH_Y = re.compile(r"\{\{birth.*(\d\d\d\d)", flags=re.I | re.DOTALL)
INFOBOX_DEATH_YMD = re.compile(r"{\{death.*(\d\d\d\d)\| *(\d+)\| *(\d+)\| *(\d\d\d\d)\| *(\d+)\| *(\d+)")
INFOBOX_LIST = re.compile(r"\|([^\|}]*)", re.DOTALL)
INFOBOX_LT_GT = re.compile(r"&lt.*&gt;", re.DOTALL)
INFOBOX_CITATION = re.compile(r"\{\{cit.*?\}\}", flags=re.I | re.DOTALL)
INFOBOX_MARRIAGE = re.compile("\{\{ *marriage *\|(.*?)\}\}", flags=re.I | re.DOTALL)
