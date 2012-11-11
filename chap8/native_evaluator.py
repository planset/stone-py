#!/usr/bin/env python
# -*- coding: utf-8 -*-
from stone.util import reviser, super
from stone import exception
from stone.myast import fun

from chap7 import function_evaluator
from chap8 import native_function


# function_evaluator.ArgumentsEx

@reviser
class NativeArgEx(function_evaluator.ArgumentsEx):
    def __init__(self, list_of_astree):
        super(NativeArgEx, self).__init__(list_of_astree)

    def eval(self, caller_env, value):
        if not value.__class__ == native_function.NativeFunction:
            return super(NativeArgEx, self).eval(caller_env, value)
        func = value
        nparams = func.num_of_parameters()
        if self.size() != nparams:
            raise exception.StoneException("bad number of arguments", self)
        args = []
        for a in self.children():
            args.append(a.eval(caller_env))
        return func.invoke(args, self)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
