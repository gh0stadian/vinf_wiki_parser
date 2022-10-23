import parser_utils.utils.regexes as regexes


def parse_single_parameter( parameter):
    split = parameter.find('=')
    var_value = remove_brackets(parameter[split + 1:])
    if var_value == '' or var_value == ' ':
        return None, None
    if var_value.startswith(" {{hlist"):
        var_value = parse_hlist(var_value)
    var_name = parameter[1:split].replace(" ", "")
    return var_name, var_value


def remove_brackets(text):
    text = text.replace("[[", '')
    return text.replace("]]", '')


def parse_hlist(text):
    text = regexes.INFOBOX_HLIST.search(text).group(1)
    text = text.replace("|", ", ")
    return text
