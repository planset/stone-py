#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone import exception


class ClassInfo(object):
    def __init__(self, cs, env):
        self.definition = cs
        self._environment = env
        obj = env.get(cs.super_class())
        if obj is None:
            self._super_class = None
        elif isinstance(obj, ClassInfo):
            self._super_class = obj
        else:
            raise exception.StoneException('unknown super class: ' + cs.super_class(), cs)

    def name(self):
        return self.definition.name()

    def super_class(self):
        return self._super_class

    def body(self):
        return self.definition.body()

    def environment(self):
        return self._environment

    def to_string(self):
        return '<class {}>'.format(self.name())


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
