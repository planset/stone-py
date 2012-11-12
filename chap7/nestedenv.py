#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chap6 import basic_env


class NestedEnv(basic_env.Environment):
    def __init__(self, env=None):
        self.values = {}
        self.outer = env

    def set_outer(self, env):
        self.outer = env

    def get(self, name):
        v = self.values.get(name)
        if v is None and self.outer is not None:
            return self.outer.get(name)
        else:
            return v

    def put_new(self, name, value):
        self.values[name] = value

    def put(self, name, value):
        env = self.where(name)
        if env is None:
            env = self
        env.put_new(name, value)

    def where(self, name):
        if self.values.get(name) is not None:
            return self
        elif self.outer is None:
            return None
        else:
            return self.outer.where(name)



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
