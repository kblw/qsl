# -*- coding: utf-8 -*-


def either(predicate, left, right):
    return predicate and left or right


def as_str(val):
    if isinstance(val, basestring):
        return "'{}'".format(val)
    return val
