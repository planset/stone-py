#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chap7 import function
from chap11 import array_env

class OptFunction(function.Function):
    def __init__(self, parameters, body, env, memory_size):
        super(OptFunction, self).__init__(parameters, body, env)
        self.size = memory_size

    def make_env(self):
        return array_env.ArrayEnv(self.size, self.env)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
