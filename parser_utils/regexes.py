import re

# DOCUMENT REGEXES
SPLIT_PAGES = re.compile(r"<page>(.*?)</page>", re.DOTALL)

# PAGE REGEXES
PAGE_GET_TITLE = re.compile(r"<title>(.*?)</title>", re.DOTALL)
PAGE_GET_OCCUPATION = re.compile(r"\| occupation *?= ({{.*?}}|.*?\n)", re.DOTALL)
PAGE_GET_INFOBOX = re.compile(r"{{Infobox.*?\n(?:[^{}]*|(?:{{.*?}}))*}}", flags=re.I | re.DOTALL)

# INFOBOX REGEXES
INFOBOX_BIRTH_YMD = re.compile(r"(\d\d\d\d)\| *(\d+)\| *(\d+)")
INFOBOX_BIRTH_Y = re.compile(r"(\d\d\d\d)")
INFOBOX_DEATH_YMD = re.compile(r"(\d\d\d\d)\| *(\d+)\| *(\d+)\| *(\d\d\d\d)\| *(\d+)\| *(\d+)")
INFOBOX_HLIST = re.compile(r" *{{hlist *\|(.*)}}")