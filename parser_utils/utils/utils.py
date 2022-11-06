import re

import parser_utils.utils.regexes as regexes


def parse_single_parameter(parameter):
    if var_val := regexes.INFOBOX_VAR_VAL.search(parameter):
        if value := var_val.group(2):
            value = remove_special_characters(value)
            name = var_val.group(1)
            if name.startswith('module'):
                return None
            if name == 'birth_date':
                value = parse_birth_date(value)
            if name == 'death_date':
                value = parse_death_date(value)
            return name, value
    return None


def parse_birth_date(text):
    if match := regexes.INFOBOX_BIRTH_YMD.search(text):
        return match.group(1) + "/" + match.group(2) + "/" + match.group(3)
    elif match := regexes.INFOBOX_BIRTH_Y.search(text):
        return match.group(1)


def parse_death_date(text):
    if match := regexes.INFOBOX_DEATH_YMD.search(text):
        return match.group(1) + "/" + match.group(2) + "/" + match.group(3)


def remove_special_characters(text):
    text = parse_lists(text)
    text = text.replace('&amp;', '&')
    text = text.replace('&ndash;', '-')
    text = text.replace('&quot;', '"')
    text = re.sub(regexes.INFOBOX_LT_GT, '', text)
    text = regexes.INFOBOX_MARRIAGE.sub(split_or, text)
    text = re.sub(regexes.INFOBOX_CITATION, '', text)
    text = remove_brackets(text)
    return text


def split_or(text):
    if text.group(1):
        return ",".join(text.group(1).split('|'))


def split_star(text):
    return (", ".join(text.split('*')[1:]))[:-2].replace('\n', '')


def remove_brackets(text):
    text = text.replace("[[", '')
    text = text.replace("\n}}", '')
    return text.replace("]]", '')


def parse_lists(text):
    if text.lower().startswith(('{{hlist', '{{URL', '{{url', '{{website', '{{marriage', '{{nobold', '{{unbulleted',
                                '{{csv', '{{nihongo', '{{ubl', '{{ill', '{{circa')):
        return ", ".join(regexes.INFOBOX_LIST.findall(text))
    if text.lower().startswith(('{{plain', '{{flat')):
        return split_star(text)
    return text


def find_singles(text):
    return []


def remove_html_tags(text):
    text = regexes.AWARDS_ROWSPAN.sub("***\\1***", text)
    return regexes.AWARDS_HTML_TAG.sub("", text)


def remove_header_footer(text):
    a = regexes.AWARDS_HEADER_1.sub("", text)
    a = regexes.AWARDS_HEADER_2.sub("", a)
    a = a.replace("\n|}", "")
    return a


def preprocess_awards(text):
    text = text.replace('&amp;', '&')
    text = text.replace('&ndash;', '-')
    text = text.replace('&quot;', '"')
    text = text.replace('\n!', '\n|')
    text = re.sub(regexes.INFOBOX_LT_GT, '', text)
    text = re.sub(regexes.INFOBOX_CITATION, '', text)
    text = re.sub(regexes.AWARDS_NOMINATED_FLAG, "Nominated", text)
    text = re.sub(regexes.AWARDS_WINNER_FLAG, "Winner", text)
    text = remove_brackets(text)
    return text
