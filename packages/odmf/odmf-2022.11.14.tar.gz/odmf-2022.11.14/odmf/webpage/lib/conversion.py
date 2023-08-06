"""
Tools to and from convert strings to numerous types
"""

import json
from datetime import datetime


def jsonhandler(obj):
    if hasattr(obj, '__jdict__'):
        return obj.__jdict__()
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return obj.__dict__


def as_json(*args, **kwargs) -> str:
    """
    Builds a JSON string representation of the given object using __jdict__ methods
    of the objects or of owned objects
    Parameters
    ----------
    obj
        The object to stringify

    Returns
    -------
    A JSON string
    """
    if len(args) == 1:
        return json.dumps(args[0], sort_keys=True, indent=4, default=jsonhandler)
    elif len(args) == 0:
        return json.dumps(kwargs, sort_keys=True, indent=4, default=jsonhandler)
    elif kwargs:
        raise ValueError('You can\'t create a json representation from mixing positional and key word arguments')
    else:
        return json.dumps(list(args), sort_keys=True, indent=4, default=jsonhandler)


def formatdate(t=None, fmt='%d.%m.%Y'):
    if not t:
        return datetime.today().strftime(fmt)
    try:
        return t.strftime(fmt)
    except (TypeError, ValueError):
        return None


def formattime(t, showseconds=True):
    try:
        return t.strftime('%H:%M:%S' if showseconds else '%H:%M')
    except (TypeError, ValueError):
        return None


def formatdatetime(t=None, fmt='%d.%m.%Y %H:%M:%S'):
    if not t:
        t = datetime.now()
    try:
        return t.strftime(fmt)
    except (TypeError, ValueError):
        return None


def formatfloat(v, style='%g'):
    try:
        return style % v
    except (TypeError, ValueError):
        return 'N/A'


def parsedate(s, raiseerror=True):
    res = None
    formats = ('%d.%m.%Y %H:%M:%S', '%d.%m.%Y %H:%M', '%d.%m.%Y', '%Y-%m-%d', '%Y-%m-%d %H:%M:%S',
               '%Y/%m/%dT%H:%M:%S', '%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S')
    for fmt in formats:
        try:
            res = datetime.strptime(s, fmt)
        except (ValueError, TypeError):
            pass
    if not res and raiseerror:
        raise ValueError('%s is not a valid date/time format' % s)
    else:
        return res


def conv(cls, s, default=None):
    """
    Convert string s to class cls
    Parameters
    ----------
    cls
        A class to convert to (eg. float, int, datetime)
    s
        A string to convert
    default
        A default answer, if the conversion fails. Else return None

    Returns
    -------
    cls(s)

    """
    if cls is datetime:
        return parsedate(s)
    try:
        return cls(s)
    except (TypeError, ValueError):
        return default


