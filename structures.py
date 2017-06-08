# -*- coding: utf-8 -*-

from helpers import either, as_str


class Point(object):
    def __init__(self, (is_include, value)):
        self.is_include = is_include
        self.value = value


class Range(object):
    def __init__(self, left_pair, right_pair):
        self.left = Point(left_pair)
        self.right = Point(right_pair)

    def __str__(self):
        return '{}{}, {}{}'.format(either(self.left.is_include, '[', '('),
                                   as_str(self.left.value),
                                   as_str(self.right.value),
                                   either(self.right.is_include, ']', ')'))

    def __repr__(self):
        return str(self)
