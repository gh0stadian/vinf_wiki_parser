import parser_utils.regexes as regexes

from parser_utils.generic_page_object import GenericPageObject


class InfoboxObject(GenericPageObject):
    def __init__(self, text):
        super().__init__(text)
        self._save_awards("data/tmp_awards")
        self._parse_birth_date()
        self._parse_death_date()

    def _parse(self, raw_infobox):
        params = raw_infobox.split("\n|")
        params_dict = {}

        if len(params) > 2:
            for parameter in params[1:-1]:
                var_name, var_value = self._parse_single_parameter(parameter)
                if var_name:
                    params_dict[var_name] = var_value
        return params_dict

    def _save_awards(self, filename):
        if 'awards' in self.parsed.keys():
            with open(filename, "a", encoding="utf8") as f:
                f.write(self.parsed['awards'] + "\n")

    def _parse_birth_date(self):
        if 'birth_date' in self.parsed.keys():
            if match := regexes.INFOBOX_BIRTH_YMD.search(self.parsed['birth_date']):
                self.parsed['birth_date'] = match.group(1) + "/" + match.group(2) + "/" + match.group(3)
            elif match := regexes.INFOBOX_BIRTH_Y.search(self.parsed['birth_date']):
                self.parsed['birth_date'] = match.group(0)
            else:
                del self.parsed['birth_date']

    def _parse_death_date(self):
        if 'death_date' in self.parsed.keys():
            if match := regexes.INFOBOX_DEATH_YMD.search(self.parsed['death_date']):
                self.parsed['death_date'] = match.group(1) + "/" + match.group(2) + "/" + match.group(3)
            else:
                del self.parsed['death_date']

    def _parse_hlist(self, text):
        text = regexes.INFOBOX_HLIST.search(text).group(1)
        text = text.replace("|", ", ")
        return text

    def _parse_single_parameter(self, parameter):
        split = parameter.find('=')
        var_value = self._remove_brackets(parameter[split + 1:])
        if var_value == '' or var_value == ' ':
            return None, None
        if var_value.startswith(" {{hlist"):
            var_value = self._parse_hlist(var_value)
        var_name = parameter[1:split].replace(" ", "")
        return var_name, var_value

    def _remove_brackets(self, text):
        text = text.replace("[[", '')
        return text.replace("]]", '')

    def __str__(self):
        o = "Infobox" + "-" * 73 + "\n"
        for key, value in self.parsed.items():
            o += f"{key}: {value}\n"
        return o + "-" * 80
