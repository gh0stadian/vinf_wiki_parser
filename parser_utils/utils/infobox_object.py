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

        if len(params) > 2:
            for parameter in params[1:-1]:
                var_name, var_value = parse_single_parameter(parameter)
                if var_name:
                    params_dict[var_name] = var_value

        return InfoboxObject(params_dict)

    def _save_awards(self, filename):
        if 'awards' in self.about.keys():
            with open(filename, "a", encoding="utf8") as f:
                f.write(self.about['awards'] + "\n")

    # def _parse_birth_date(self):
    #     if 'birth_date' in self.parsed.keys():
    #         if match := regexes.INFOBOX_BIRTH_YMD.search(self.parsed['birth_date']):
    #             self.parsed['birth_date'] = match.group(1) + "/" + match.group(2) + "/" + match.group(3)
    #         elif match := regexes.INFOBOX_BIRTH_Y.search(self.parsed['birth_date']):
    #             self.parsed['birth_date'] = match.group(0)
    #         else:
    #             del self.parsed['birth_date']

    # def _parse_death_date(self):
    #     if 'death_date' in self.parsed.keys():
    #         if match := regexes.INFOBOX_DEATH_YMD.search(self.parsed['death_date']):
    #             self.parsed['death_date'] = match.group(1) + "/" + match.group(2) + "/" + match.group(3)
    #         else:
    #             del self.parsed['death_date']

    def __str__(self):
        o = "About".ljust(80, "-") + "\n"
        for key, value in self.about.items():
            o += " " * 5 + f"{key}: {value}\n"
        return o
