from collections import OrderedDict
import json
import copy
from difflib import ndiff

odict = OrderedDict


class DictUtil(object):
    def __init__(self, _dict=None):
        self._dict = _dict

    def sorted(self):
        return OrderedDict(sorted(self._dict.items()))

    @classmethod
    def merge(cls, *dict_args):
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def key_value_tuples(self):

        return [(key, value) for key, value in self._dict.iteritems()]

    def key_value_output(self):

        output = ''
        for _tuple in self.key_value_tuples():
            output += str(_tuple)
            output += '\n'

        return output

    def to_json_string(self):

        return json.dumps(self._dict)

    def to_pretty_json_string(self):

        return json.dumps(self._dict, indent=4)

    pprint = to_pretty_json_string

    def first_value(self):

        return self._dict.items()[0][1]

    def second_value(self):

        return self._dict.items()[1][1]

    def copy(self):

        dict_copy = copy.deepcopy(self._dict)

        return dict_copy

    def add_odicts(self, dict1, dict2):
        dicts_items_sum = [(key, dict1[key] + dict2[key]) for key in set(dict1) & set(dict2)]
        return odict(dict1.items() + dict2.items() + dicts_items_sum)

    def has_truthy_values(self):

        return all(self._dict.values())

    def has_no_none_values(self):

        return None not in self._dict.values()

    def diff(self, odict1, odict2):

        raw_diff = ndiff(
            pretty_json_string_from(odict1).splitlines(1),
            pretty_json_string_from(odict2).splitlines(1)
        )
        diff = ''.join(raw_diff)

        return diff

    @staticmethod
    def keys_to_lowercase(x, order_dict=False):
        """

        :param x: dict
        :param order_dict: (bool) To return a dict or an order dict
        :return: convert all the keys of dict to lower key include it's children
        """
        if isinstance(x, list):
            return [DictUtil().keys_to_lowercase(v, order_dict) for v in x]
        elif isinstance(x, dict):
            if order_dict:
                return OrderedDict((k.lower(), DictUtil().keys_to_lowercase(v, order_dict)) for k, v in x.iteritems())
            else:
                return dict((k.lower(), DictUtil().keys_to_lowercase(v, order_dict)) for k, v in x.iteritems())
        else:
            return x

    @staticmethod
    def dict_compare(d1, d2):
        """

        :type d1: dict
        :type d2: dict
        :return: A dict with details of the common and diff between two dicts
        """
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        intersect_keys = d1_keys.intersection(d2_keys)
        added = d1_keys - d2_keys
        removed = d2_keys - d1_keys
        modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
        same = set(o for o in intersect_keys if d1[o] == d2[o])
        return dict(added=added, removed=removed, modified=modified, same=same)

    def filter_keys_that_start_with(self, string):

        filtered_dict = {key: value for key, value in self._dict.iteritems() if key.startswith(string)}

        return filtered_dict


Dict = DictUtil


def jsonify(_dict):
    return DictUtil(_dict).to_json_string()


def pretty_json_string_from(dictionary):
    return DictUtil(dictionary).to_pretty_json_string()
