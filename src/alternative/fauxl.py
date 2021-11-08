"""
Fauxlizer
"""

import sys
import csvreader as csv
import json
from math import floor
from cleanup import explode, prop
from cat_theory import compose, fold, tryCatch, Nothing

sys.path.append("../")


class Schema:
    """ semi-group to allow for composing validation checks """

    def __init__(self, x):
        self.x = x

    def contents(self):
        return self.x

    def check(self, predicate):
        if self.x != {} and self.x != [""] and predicate(self.x) == True:
            return Schema(self.x)
        else:
            return Schema({})

    def __repr__(self):
        return "Schema({0})".format(self.x)


""" Fauxlizer Util Methods """


def clean_headers(headers):
    no_newlines = lambda x: x.replace("\n", "")
    strip = lambda x: x.strip()
    clean = compose(strip, no_newlines)
    return [clean(header) for header in headers]


def get_headers(reader):
    headers = lambda x: x["headers"]
    new_headers = compose(compose(clean_headers, headers), csv.get_headers)
    existing_headers = compose(clean_headers, headers)
    if reader["headers"] == []:
        return new_headers(reader)
    else:
        return existing_headers(reader)


def parse(data_invariant_and_headers):
    """ data_invariant_and_headers ==  tuple(Schema(), headers) """
    data_invariant = data_invariant_and_headers[0]
    headers = data_invariant_and_headers[1]

    if data_invariant.contents() != {}:
        d = data_invariant.contents()
        results = {}
        for idx, header in enumerate(headers):
            results[header] = d[idx]
        return results
    else:
        return {}


def parse_line(headers):
    def apply(line):
        """ ex. {experiment_name: 'examination.76377',
                sample_id: 449491,
                fauxness: 0.651592972723,
                category_guess: 'fake'} """
        data = explode(line, ",")
        return compose(parse, schema_check)((headers, data))

    return apply


def parse_type(fn, data):
    maybe_type = tryCatch(fn, data)
    return type(maybe_type) is not Nothing


def schema_keys(data):
    return (
        "experiment_name" in data
        and "sample_id" in data
        and "fauxness" in data
        and "category_guess" in data
    )


def schema_values(data):
    lower = lambda x: x.lower()
    strip = lambda x: x.strip()
    clean = compose(strip, lower)

    def category_guess(x):
        val = clean(x)
        return val == "real" or val == "fake" or val == "ambiguous"

    return (
        parse_type(lambda d: int(d[1]), data)
        and parse_type(lambda d: float(d[2]), data)
        and category_guess(data[3])
    )


def schema_check(headers_and_data):
    """ headers_and_data == tuple(headers, data) """
    headers = headers_and_data[0]
    data = headers_and_data[1]
    return (
        Schema(data)
        .check(lambda d: d is not [""])
        .check(lambda d: len(d) == 4)
        .check(lambda d: schema_keys(headers))
        .check(lambda d: schema_values(d)),
        headers,
    )


""" Summary functions """


def sort_by_fauxness(key_and_lst):
    """ key_and_lst == tuple(key, lst) """
    key = key_and_lst[0]
    lst = key_and_lst[1]

    # merge sort on the schema key's value
    if len(lst) < 2:
        return lst
    mid = floor(len(lst) / 2)
    left = sort_by_fauxness((key, lst[mid:]))
    right = sort_by_fauxness((key, lst[:mid]))

    # merge
    i = j = 0
    sorted_list = []
    obj_prop = compose(float, prop(key))

    while len(sorted_list) < len(lst):
        if (
            j >= len(right)
            or i < len(left)
            and left[i] != {}
            and right[j] != {}
            and obj_prop(left[i]) < obj_prop(right[j])
        ):
            sorted_list.append(left[i])
            i += 1
        elif j < len(right):
            sorted_list.append(right[j])
            j += 1
    return sorted_list


def sum_by_fauxness(schema_key_and_data):
    """ schema_key_and_data == tuple(schema_key, data) """
    schema_key = schema_key_and_data[0]
    data = schema_key_and_data[1]
    fauxness = compose(float, prop(schema_key))
    reducer = lambda acc, x: acc + fauxness(x)
    return fold(reducer, 0.0, data)


""" Fauxlizer API Methods """


def parse_file(filename=None):
    if filename is None:
        return []
    rdr = csv.make_reader(filename)
    rdr["headers"] = get_headers(rdr)
    rdr = csv.parse_file(rdr, parse_line(rdr["headers"]))
    rdr = csv.close_reader(rdr)
    return rdr["data"]


def pluck_item_as_json(index, data):
    toJson = compose(json.dumps, prop(index))
    if index <= len(data) - 1:
        return toJson(data)
    else:
        return json.dumps({})


def summary_by_fauxness(filename=None):
    empty_summary = {}
    if filename is None:
        return empty_summary
    d = parse_file(filename)
    if validate_data(d):
        sorted_data = sort_by_fauxness(("fauxness", d))
        filtered_lst = []
        for item in sorted_data:
            if "fauxness" in item:
                filtered_lst.append(item)
        while True:
            if filtered_lst[len(filtered_lst) - 1] == {}:
                del filtered_lst[len(filtered_lst) - 1]
            else:
                break
        return {
            "SUMMARY": "fauxness",
            "SUM": sum_by_fauxness(("fauxness", filtered_lst)),
            "MIN": filtered_lst[0]["fauxness"],
            "MAX": filtered_lst[len(filtered_lst) - 1]["fauxness"],
        }
    else:
        return empty_summary


def validate(filename=None):
    if filename is None:
        return False
    d = parse_file(filename)
    return validate_data(d)


def validate_data(d):
    valid = False
    for item in d:
        if item != {}:
            valid = True
            break
    return valid


""" Runner """


def main(fauxlizer_file):
    # parse
    data = parse_file(fauxlizer_file)
    print("Fauxlizer run for data file: {0} \n".format(fauxlizer_file))
    print(data)
    # validate
    print("Is data file valid? {0} \n".format(validate(fauxlizer_file)))
    # summary
    print(summary_by_fauxness(fauxlizer_file))
    # retrieve row by alternate format
    print(pluck_item_as_json(0, data))


if __name__ == "__main__":
    main("../../data_files/file_1.faux")  # valid
    print("\n")
    main("../../data_files/file_3.faux")  # invalid
