"""
A lite version of generic csv module, the name is
just to distinguish it from the built_in csv module
"""

from cat_theory import Some, tryCatch


class AmyrisCsv:
    def __init__(self, filename=None):

        self.filename = filename
        self.empty_data = [{}]
        self.empty_headers = []
        if filename is None:
            self.headers = self.empty_headers
            return

        maybe_headers = tryCatch(self.cache_headers, filename)
        if type(maybe_headers) is Some:
            self.headers = maybe_headers.contents()
        else:
            self.headers = []

    def cache_headers(self, filename):
        if filename is None:
            return self.empty_headers

        f = open(filename)
        line = f.readline()
        f.close()
        return line.split(",")

    def parse_data_file(self, parser):
        if self.filename is None or self.headers is self.empty_headers:
            return self.empty_data
        f = open(self.filename)
        line = f.readline()
        output = []
        while line:
            line = f.readline()
            output.append(parser(line))
        f.close()
        return output
