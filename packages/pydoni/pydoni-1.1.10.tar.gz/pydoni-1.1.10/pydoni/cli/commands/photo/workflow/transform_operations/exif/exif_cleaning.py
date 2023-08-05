import ast
import re
import numpy as np
import pandas as pd


def isnull(x):
    """
    Return boolean indicating whether a value is null.
    """
    if pd.isnull(x):
        return True
    elif str(x).lower() in ['nan', 'none', 'null', 'n/a']:
        return True
    else:
        return False


def map_on_off(x):
    """
    Map 'On' to True and 'Off' to False.
    """
    if str(x).lower() == 'on':
        return True
    elif str(x).lower() == 'off':
        return False
    else:
        return None


def str_replace(x, pat, repl):
    """
    Apply .replace() string method to a value.
    """
    if isnull(x):
        return x
    else:
        return str(x).replace(pat, repl)


def str_strip(x):
    """
    Apply .strip() string method to a value.
    """
    if isnull(x):
        return x
    else:
        return str(x).strip()


def value_map(x, mapping):
    """
    If value `x` is found in `mapping.keys()`, return the mapped value.
    """
    for k, v in mapping.items():
        if x == k:
            if isnull(v):
                mapped_v = None
            else:
                mapped_v = v

            return mapped_v

    return x


def is_list_stored_as_string(x):
    """
    Determine whether a value is a list stored as a strong.
    """
    if '[' in str(x) and ']' in str(x):
        try:
            lst_x = ast.literal_eval(str(x))
            is_list = isinstance(lst_x, list)
            assert is_list, "Expected list for the following vlaue: " + str(x)
            return True
        except:
            return False
    else:
        return False


def to_numeric(x):
    """
    Coerce a string value to numeric. Preserve NaNs. Numerically evaluate fractions.
    """
    if isnull(x):
        return np.NaN
    elif re.match(r'^(-|\+)?\d+\/\d+$', str(x)):
        return eval(x)
    else:
        return pd.to_numeric(x)


def first_list_item(x):
    """
    Extract the first item from a list value stored as a string. For example, take
    the sample value "['45', '30']" and extract '45'.
    """
    if is_list_stored_as_string(x):
        lst_x = ast.literal_eval(str(x))
        return(lst_x[0])
    else:
        return x


def first_item_split_on_space(x):
    """
    Brute force extract the first part of a string before a space.
    """
    return str(x).split()[0]


def str_remove(x, remove_lst):
    """
    Remove specified strings from a value.
    """
    remove_lst = [remove_lst] if not isinstance(remove_lst, list) else remove_lst

    for item in remove_lst:
        x = str(x).replace(item, '')

    return x


def parse_dms(dms, extract='both'):
    """
    Parse a GPS Position string to a (lat, lng) tuple. `extract` parameter may be
    one of 'lat', 'lng' or 'both'. If 'lat' or 'lng', this function will treat
    the input value (`dms`) as if 
    """

    # def dd2dms(deg):
    #     d = int(deg)
    #     md = abs(deg - d) * 60
    #     m = int(md)
    #     sd = (md - m) * 60
    #     return [d, m, sd]


    def dms2dd(degrees, minutes, seconds, direction):
        dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
        if direction == 'S' or direction == 'W':
            dd *= -1
        return dd


    if isnull(dms):
        if extract in ['lat', 'lng']:
            return np.NaN
        else:
            return (np.NaN, np.NaN)

    dms = str(dms)
    dms = dms.replace('"', '"').replace('deg', '°')
    dms = dms.split(',')
    dms = [x.replace(' ', '') for x in dms]
    dms = [x[:len(x)-1] + ' ' + x[len(x)-1] for x in dms]
    dms = ' '.join(dms)

    parts = re.split(r'[^\d\w\.]+', dms)
    if len(parts) == 8:
        # Full latitude/longitude coordinates supplied
        dms_type = 'full'
    elif len(parts) == 4:
        # Either just latitude or longitude supplied
        dms_type = 'partial'
    else:
        raise Exception(f"Unrecognized dms type for value '{dms}'")


    if dms_type == 'full':
        # Standard case
        lat = dms2dd(parts[0], parts[1], parts[2], parts[3])
        lng = dms2dd(parts[4], parts[5], parts[6], parts[7])

        if extract == 'lat':
            return lat
        elif extract == 'lng':
            return lng
        else:
            return (lat, lng)

    elif dms_type == 'partial':
        assert not extract == 'both', \
            f"Cannot extract both latitude and longitude from partially supplied `dms` value '{dms}'"
        
        lat_or_lng = dms2dd(parts[0], parts[1], parts[2], parts[3])
        return lat_or_lng


parse_dms_lat = lambda dms: parse_dms(dms, extract='lat')
parse_dms_lng = lambda dms: parse_dms(dms, extract='lng')


def parse_shutter_type(x):
    """
    Get the shutter type as 'Mechanical', 'Electronic' or 'Other'.
    """
    if 'mechanical' in str(x).lower():
        return 'Mechanical'
    elif 'electronic' in str(x).lower():
        return 'Electronic'
    else:
        return 'Other'


def algebraic_operation(x, operator, number):
    """
    Apply an algebraic operation to a value. 'operator' must be one of 'add',
    'subtract', 'multiply' or 'divide'.
    """
    assert operator in ['add', 'subtract', 'multiply', 'divide']
    if isnull(x):
        return np.NaN
    elif operator == 'add':
        return x + number
    elif operator == 'subtract':
        return x - number
    elif operator == 'multiply':
        return x * number
    elif operator == 'divide':
        return x / number