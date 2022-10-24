from parser_utils.utils.utils import *

class InfoboxObject():
    def __init__(self, about_dict):
        self.about = about_dict
        # self._save_awards("data/tmp_awards")
        # self._parse_birth_date()
        # self._parse_death_date()

    @classmethod
    def from_raw(cls, raw_infobox):
        params = raw_infobox.split("\n|")
        params_dict = {}

        for parameter in params[1:]:
            if var_value := parse_single_parameter(parameter):
                params_dict[var_value[0]] = var_value[1]
        return InfoboxObject(params_dict)

    def _save_awards(self, filename):
        if 'awards' in self.about.keys():
            with open(filename, "a", encoding="utf8") as f:
                f.write(self.about['awards'] + "\n")
    def __str__(self):
        o = "About".ljust(80, "-") + "\n"
        for key, value in self.about.items():
            o += " " * 5 + f"{key}: {value}\n"
        return o
