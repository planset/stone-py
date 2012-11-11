#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect
from stone import exception


class NativeFunction(object):
    def __init__(self, name, method):
        self.name = name
        self.method = method
        argspec = inspect.getargspec(method)
        self.num_params = len(argspec.args)

    def to_string(self):
        return "<native:{}>".format(self.__hash__())

    def num_of_parameters(self):
        return self.num_params

    def invoke(self, args, tree):
        try:
            if len(args) == 0:
                return self.method()
            return self.method(args)
        except:
            raise exception.StoneException("bad native function call: {}".format(self.name),
                                           tree)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


