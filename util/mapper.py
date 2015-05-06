from schemas.common import *

def upper_to_lower_camel(string):
    first_letter = string[0]
    return first_letter.lower() + string[1:]

def lower_to_upper_camel(string):
    first_letter = string[0]
    return first_letter.upper() + string[1:]

def convert_keys(d, convert):
    new_d = {}
    for k, v in d.items():
        new_d[convert(k)] = convert_keys(v,convert) if isinstance(v,dict) else v
    return new_d


if __name__ == '__main__':

    x = {}

    print(convert_keys(x, upper_to_lower_camel))