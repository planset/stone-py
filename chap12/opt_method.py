#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chap11 import array_env, opt_function

class OptMethod(opt_function.OptFunction):
    def __init__(self, parameters, body, env, memory_size, _self):
        super(OptMethod, self).__init__(parameters, body, env, memory_size)
        self.self = _self

    def make_env(self):
        e = array_env.ArrayEnv(self.size, self.env)
        e.put(0, 0, self.self)
        return e


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
    

