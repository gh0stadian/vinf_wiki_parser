from parser_utils.utils.utils import *

class InfoboxObject():
    def __init__(self, about_dict):
        self.about = about_dict

    @classmethod
    def from_raw(cls, raw_infobox):
        """Creates an InfoboxObject from a raw infobox string."""
        params = raw_infobox.split("\n|")
        params_dict = {}

        for parameter in params[1:]:
            if var_value := parse_single_parameter(parameter):
                params_dict[var_value[0]] = var_value[1]
        return InfoboxObject(params_dict)

    def __str__(self):
        """Returns a string representation of the object."""
        o = "About".ljust(80, "-") + "\n"
        for key, value in self.about.items():
            o += " " * 5 + f"{key}: {value}\n"
        return o
