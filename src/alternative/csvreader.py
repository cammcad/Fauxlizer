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
    if reader["file_handle"] is None:
        return reader
    elif reader["headers"] == []:
        line = reader["file_handle"].readline()
        reader["headers"] = explode(line, ",")
        return reader


def make_reader(filename=None):
    maybe_file = tryCatch(get_file_handle, filename)
    if type(maybe_file) is Some:
        return {"headers": [], "file_handle": maybe_file.contents(), "data": [{}]}
    else:
        return {"headers": [], "file_handle": None, "data": [{}]}


def parse_file(reader, parser):
    if reader["file_handle"] is None:
        return reader
    elif reader["headers"] == []:
        reader = get_headers(reader)
    line = reader["file_handle"].readline()
    output = []
    while line:
        line = reader["file_handle"].readline()
        output.append(parser(line))
    reader["data"] = output
    return reader


def close_reader(reader):
    reader["file_handle"].close()
    reader["file_handle"] = None
    return reader
