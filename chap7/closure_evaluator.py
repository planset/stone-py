# -*- coding: utf-8 -*-

from stone.util import reviser
from stone.myast import fun

#from chap6 import basic_env
#from chap6 import basic_evaluator
from chap7 import function
from chap7 import function_evaluator

@reviser
class FunEx(fun.Fun):
    def __init__(self, list_of_astree):
        super(FunEx, self).__init__(list_of_astree)

    def eval(self, env):
        return function.Function(self.parameters(), self.body(), env)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
