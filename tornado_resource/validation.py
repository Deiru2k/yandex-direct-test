import functools
import json
import re

from tornado.gen import coroutine

from jsonschema import Draft4Validator
from bson import json_util as bjson
from tornado_resource.resource import APIError


rx = [
    re.compile(r"'(\w+|\d+)' is a required property"),
    re.compile(r"Additional properties are not allowed \('(\w+|\d+)' was unexpected\)")
]

def one_of_instance(obj, type_list=[]):

    for type_ in type_list:
        if isinstance(obj, type_):
            return True
    return False


def _validate_schema(schema, data):
    validator = Draft4Validator(schema)
    try:
        if isinstance(data, bytes):
            data = json.loads(data.decode("UTF-8"))
        if isinstance(data, str):
            data = json.loads(data.encode("UTF-8"))
        elif one_of_instance(data, [dict, list, tuple, int, float]):
            data = json.loads(bjson.dumps(data))
        else:
            raise APIError(code=400, message="Malformed JSON")
    except (ValueError, AttributeError, UnicodeError):
        raise APIError(code=400, message="Malformed JSON", data=data)
    if not validator.is_valid(data):
        raise APIError(code=400, message="Could not validate JSON", errors=format_errors(validator.iter_errors(data)))
    return data


def validate(input_schema=None, output_schema=None):
    def decorator(f):
        @coroutine
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            self._auto_finish = False
            if input_schema:
                data = _validate_schema(input_schema, self.request.body)
                setattr(self, "input", data)
            result = yield f(self, *args, **kwargs)
            if output_schema:
                _validate_schema(output_schema, result[1])
            return result
        return wrapper
    return decorator


def update_dict(d, nd):

    copy = d
    copy.update(nd)
    return copy


def format_errors(errors):

    plain_errors = dict()
    for error in errors:
        check = check_regex(error.message)
        if check:
            error.absolute_path.append(check)
        path = list()
        for key in error.absolute_path:
            path.append(str(key))
        key = ".".join(path)
        plain_errors[key] = error.message
    return plain_errors


def check_regex(message):
    for r in rx:
        search = r.search(message)
        if search:
            return search.group(1)
    return None