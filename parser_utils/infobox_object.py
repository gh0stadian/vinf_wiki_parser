from parser_utils.generic_page_object import GenericPageObject


class InfoboxObject(GenericPageObject):
    def __init__(self, text):
        super().__init__(text)
        self._save_awards("data/tmp_awards")

    def _parse(self, raw_infobox):
        params = raw_infobox.split("\n")
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

    def _parse_single_parameter(self, parameter):
        split = parameter.find('=')
        var_value = parameter[split + 1:]
        if var_value == '' or var_value == ' ':
            return None, None
        var_name = parameter[1:split].replace(" ", "")
        return var_name, parameter[split + 1:]

    def __str__(self):
        o = "Infobox" + "-" * 73 + "\n"
        for key, value in self.parsed.items():
            o += f"{key}: {value}\n"
        return o + "-" * 80
