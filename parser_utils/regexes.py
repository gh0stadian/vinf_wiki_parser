import re

# DOCUMENT REGEXES
SPLIT_PAGES = re.compile(r"<page>(.*?)</page>", re.DOTALL)

# PAGE REGEXES
PAGE_GET_TITLE = re.compile(r"<title>(.*?)</title>", re.DOTALL)
PAGE_GET_REVISIONS = re.compile(r"<revision>(.*?)</revision>", re.DOTALL)
PAGE_GET_OCCUPATION = re.compile(r"\| occupation *?= ({{.*?}}|.*?\n)", re.DOTALL)
PAGE_GET_TEXT = re.compile(r"<text(.*?)>(.*?)</text>", re.DOTALL)
# PAGE_GET_INFOBOX = re.compile(r"{{Infobox.*?\n(?:{{.*?}})*}}", flags=re.I | re.DOTALL)
PAGE_GET_INFOBOX = re.compile(r"{{Infobox.*?\n(?:[^{}]*|(?:{{.*?}}))*}}", flags=re.I | re.DOTALL)
REVISION_GET_INFOBOXES = re.compile(r"\{\{(?:[^{{]|\{\{.*?\}\})*\}\}", re.MULTILINE)
