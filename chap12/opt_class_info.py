#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone.myast import statement
from chap9 import class_info
from chap12 import opt_method


class OptClassInfo(class_info.ClassInfo):
    def __init__(self, cs, env, methods, fields):
        super(OptClassInfo, self).__init__(cs, env)
        self.methods = methods
        self.fields = fields
        self.method_defs = None

    def size(self):
        return self.fields.size()

    def copy_to(self, f, m, mlist):
        f.append(self.fields)
        m.append(self.methods)
        for _def in self.method_defs:
            mlist.append(_def)

    def field_index(self, name):
        return self.fields.find(name)

    def method_index(self, name):
        return self.methods.find(name)

    def method(self, _self, index):
        _def = self.method_defs[index]
        return opt_method.OptMethod(_def.parameters(), _def.body(), 
                self.environment(), _def.locals(), _self)

    def set_methods(self, methods):
        self.method_defs = methods

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
