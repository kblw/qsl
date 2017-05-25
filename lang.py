# -*- coding: utf-8 -*-

import re
from dateutil.parser import parse as date_parse

OK = 0
ERROR = 1

VAR_MATCH = re.compile("^(-?)([a-zA-Z]\w*)$")
LIST_MATCH = re.compile("^(((.+?),)+)(.+?)$")
INTERVAL_MATCH = re.compile("^(.*?)\.\.(.*?)$")


def variable_parser(input):
    m = VAR_MATCH.match(input)
    if m:
        return OK, m.groups(), ''
    else:
        return ERROR, 'Unexpected variable: {}'.format(input), input


def atom_parser(input):
    try:
        return OK, int(input), ''
    except:
        try:
            return OK, float(input), ''
        except:
            try:
                return OK, date_parse(input), ''
            except:
                return OK, input, ''


def list_parser(input):
    if LIST_MATCH.match(input) is None:
        return ERROR, '', input

    result = []

    for expr in input.split(","):
        tag, output, _ = expression_parser(expr)
        if tag is ERROR:
            return tag, "Unexpected expression: {}".format(expr), input

        result.append(output)

    return OK, result, ''


def interval_parser(input):
    if INTERVAL_MATCH.match(input) is None:
        return ERROR, '', input

    result = []

    for expr in input.split('..'):
        tag, output, _ = expression_parser(expr)
        if tag is ERROR:
            return tag, "Unexpected expression: {}".format(expr), input
        result.append(output or None)

    return OK, tuple(result), ''


def expression_parser(input):
    input = input.strip()
    for parser in [list_parser, interval_parser, atom_parser]:
        tag, output, input = parser(input)
        if tag is OK:
            return tag, output, input


def parser(input):
    result = {'filters': {}, 'excludes': {}}
    for query in input.split(';'):
        try:
            var, expr = query.split(":", 1)
            tag, output, _ = variable_parser(var.strip())
            if tag is OK:
                p, var = output
                path = 'filters' if not p else 'excludes'
                tag, output, _ = expression_parser(expr)
                if tag is OK:
                    result[path][var] = output
                else:
                    raise SyntaxError(output)
            else:
                raise SyntaxError(output)
        except ValueError:
            raise SyntaxError("Unexpected subquery: {}".format(query))
    return result
