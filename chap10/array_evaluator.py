#!/usr/bin/env python
# -*- coding: utf-8 -*-
from stone.util import reviser, super
from stone import exception
from stone.myast import expression, literal, fun

from chap6 import basic_evaluator
from chap7 import function_evaluator


@reviser
class ArrayLitEx(literal.ArrayLiteral):
    def __init__(self, list_of_astree):
        super(ArrayLitEx, self).__init__(list_of_astree)

    def eval(self, env):
        #s = self.num_children()
        #res = []
        #i = 0
        #for t in self.children():
        #    res[i] = t.eval(env)
        #return res
        return [ t.eval(env) for t in self.children() ]

@reviser
class ArrayRefEx(fun.ArrayRef):
    def __init__(self, list_of_astree):
        super(ArrayRefEx, self).__init__(list_of_astree)

    def eval(self, env, value):
        if isinstance(value, list):
            index = self.index().eval(env)
            if isinstance(index, int):
                return value[index]
        raise exception.StoneException('bad array access', self)

@reviser
class AssignEx(basic_evaluator.BinaryEx):
    def __init__(self, list_of_astree):
        super(AssignEx, self).__init__(list_of_astree)

    def compute_assign(self, env, rvalue):
        le = self.left()
        if isinstance(le, expression.PrimaryExpr):
            p = le
            if p.has_postfix(0) and isinstance(p.postfix(0), fun.ArrayRef):
                a = le.eval_sub_expr(env, 1)
                if isinstance(a, list):
                    aref = p.postfix(0)
                    index = aref.index().eval(env)
                    if isinstance(index, int):
                        a[index] = rvalue
                        return rvalue
                raise exception.StoneException('bad array access', self)
        return super(AssignEx, self).compute_assign(env, rvalue)



