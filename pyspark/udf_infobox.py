import re

from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def parse_infobox(body):
    """Parses infobox from text."""
    PAGE_GET_INFOBOX = re.compile(r"\{\{Infobox(?:(?:\{\{(?:(?:\{\{(?:[^{}])*\}\})|(?:[^{}]))*\}\})|(?:[^{}]))*\}\}",
                                  flags=re.I | re.DOTALL)
    INFOBOX_VAR_VAL = re.compile(r"(\S*)\s*=\s*(.*)", re.DOTALL)
    INFOBOX_BIRTH_YMD = re.compile(r"\{\{birth.*(\d\d\d\d)\| *(\d+)\| *(\d+)", flags=re.I | re.DOTALL)
    INFOBOX_BIRTH_Y = re.compile(r"\{\{birth.*(\d\d\d\d)", flags=re.I | re.DOTALL)
    INFOBOX_DEATH_YMD = re.compile(r"{\{death.*(\d\d\d\d)\| *(\d+)\| *(\d+)\| *(\d\d\d\d)\| *(\d+)\| *(\d+)")
    INFOBOX_LIST = re.compile(r"\|([^\|}]*)", re.DOTALL)
    INFOBOX_LT_GT = re.compile(r"&lt.*?&gt;", re.DOTALL)
    INFOBOX_CITATION = re.compile(r"\{\{cit.*?\}\}", flags=re.I | re.DOTALL)
    INFOBOX_MARRIAGE = re.compile("\{\{ *marriage *\|(.*?)\}\}", flags=re.I | re.DOTALL)

    def parse_birth_date(text):
        """Parses birth date from text."""
        if match := INFOBOX_BIRTH_YMD.search(text):
            return match.group(1) + "/" + match.group(2) + "/" + match.group(3)
        elif match := INFOBOX_BIRTH_Y.search(text):
            return match.group(1)
    
    def parse_death_date(text):
        """Parses death date from text."""
        if match := INFOBOX_DEATH_YMD.search(text):
            return match.group(1) + "/" + match.group(2) + "/" + match.group(3)
    
    def remove_special_characters(text):
        """Removes special characters from text."""
        text = remove_brackets(text)
        text = parse_lists(text)
        text = text.replace('&amp;', '&')
        text = text.replace('&ndash;', '-')
        text = text.replace('&quot;', '"')
        text = re.sub(INFOBOX_LT_GT, '', text)
        text = INFOBOX_MARRIAGE.sub(split_or, text)
        text = re.sub(INFOBOX_CITATION, '', text)
        return text
    
    def split_or(text):
        """Splits text by '|'."""
        if text.group(1):
            return ",".join(text.group(1).split('|'))
        
    def split_star(text):
        """Splits text by '*'."""
        return (", ".join(text.split('*')[1:]))[:-2].replace('\n', '')
    
    def remove_brackets(text):
        """Removes brackets from text."""
        text = text.replace("[[", '')
        return text.replace("]]", '')
    
    def parse_lists(text):
        """Parses lists from text."""
        if text.lower().startswith(('{{hlist', '{{URL', '{{url', '{{website', '{{marriage', '{{nobold', '{{unbulleted',
                                    '{{csv', '{{nihongo', '{{ubl', '{{ill', '{{circa')):
            return ", ".join(INFOBOX_LIST.findall(text))
        if text.lower().startswith(('{{plain', '{{flat')):
            return split_star(text)
        return text

    infobox = PAGE_GET_INFOBOX.findall(body)
    if not infobox:
        return "{}"
    params = infobox[0].split("\n|")
    params_dict = {}
    for parameter in params[1:]:
        if var_val := INFOBOX_VAR_VAL.search(parameter):
            if value := var_val.group(2):
                value = remove_special_characters(value)
                name = var_val.group(1)
                if name.startswith('module'):
                    continue
                if name == 'birth_date':
                    value = parse_birth_date(value)
                if name == 'death_date':
                    value = parse_death_date(value)
                params_dict[name] = value
        continue
    return str(params_dict)