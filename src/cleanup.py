"""
Clean Up

Utility module to aid in cleaning up verbose and laborious syntax
"""


def explode(str, delim):
    return str.split(delim)


def prop(property):
    def apply(object):
        return object[property]

    return apply
