"""
CSV Reader
"""

import sys

sys.path.append("../")


from cat_theory import Some, tryCatch
from cleanup import explode


def get_file_handle(filename):
    if filename is None:
        return None
    return open(filename)


def get_headers(reader):
    if reader["file_handle"] is None or reader["headers"] != []:
        return reader
    else:
        line = reader["file_handle"].readline()
        return {
            "headers": explode(line, ","),
            "file_handle": reader["file_handle"],
            "data": reader["data"],
        }


def make_reader(filename=None):
    maybe_file = tryCatch(get_file_handle, filename)
    if type(maybe_file) is Some:
        return {"headers": [], "file_handle": maybe_file.contents(), "data": [{}]}
    else:
        return {"headers": [], "file_handle": None, "data": [{}]}


def parse_file(reader, parser):
    if reader["file_handle"] is None:
        return reader
    hdrs = get_headers(reader)
    line = reader["file_handle"].readline()
    output = []
    while line:
        line = reader["file_handle"].readline()
        output.append(parser(line))
    return {
        "headers": hdrs["headers"],
        "file_handle": reader["file_handle"],
        "data": output,
    }


def close_reader(reader):
    if reader["file_handle"] is None:
        return reader
    reader["file_handle"].close()
    return {"headers": reader["headers"], "file_handle": None, "data": reader["data"]}
