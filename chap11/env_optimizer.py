#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone.util import reviser, super

from stone.myast import ast, statement, fun, literal
from stone import exception
from chap6 import basic_evaluator, basic_env
from chap7 import closure_evaluator
from chap11 import opt_function, symbols


@reviser
class EnvEx2(basic_env.Environment):
    pass

@reviser
class ASTreeOptEx(ast.ASTree):
    def lookup(self, syms):
        pass

@reviser
class ASTListEx(ast.ASTList):
    def __init__(self, list_of_astree):
        super(ASTListEx, self).__init__(list_of_astree)

    def lookup(self, syms):
        for t in self.children():
            t.lookup(syms)

@reviser
class DefStmntEx(statement.DefStmnt):
    def __init__(self, list_of_astree):
        super(DefStmntEx, self).__init__(list_of_astree)

    def lookup(self, syms):
        self.index = syms.put_new(self.name())
        self.size = FunEx.lookup_by_symbols_params_body(syms, 
                        self.parameters(), self.body())

    def eval(self, env):
        env.put(0, self.index, 
                opt_function.OptFunction(self.parameters(),
                    self.body(), env, self.size))
        return self.name()

@reviser
class FunEx(fun.Fun):
    def __init__(self, list_of_astree):
        super(FunEx, self).__init__(list_of_astree)
        self.size = -1

    @staticmethod
    def lookup_by_symbols_params_body(syms, params, body):
        new_syms = symbols.Symbols(syms)
        params.lookup(new_syms)
        #revise(body).lookup(new_syms)
        body.lookup(new_syms)
        return new_syms.size()

    def lookup(self, syms):
        self.size = self.lookup(syms, self.parameters(), self.body())

    def eval(self, env):
        return opt_function.OptFunction(
                self.parameters(), self.body(), env, self.size())

@reviser
class ParamsEx(fun.ParameterList):
    def __init__(self, list_of_astree):
        super(ParamsEx, self).__init__(list_of_astree)
        self.offsets = None

    def lookup(self, syms):
        s = self.size()
        self.offsets = [None for i in range(s)]
        for i in range(s):
            self.offsets[i] = syms.put_new(self.name(i))

    def eval(self, env, index, value):
        env.put(0, self.offsets[index], value)

@reviser
class NameEx(literal.Name):
    UNKNOWN = -1
    def __init__(self, token):
        super(NameEx, self).__init__(token)

    def lookup(self, syms):
        loc = syms.get(self.name())
        if loc is None:
            raise exception.StonExcepion(
                    'undefined name: '.format(self.name()), self)
        else:
            self.nest = loc.nest
            self.index = loc.index

    def lookup_for_assign(self, syms):
        loc = syms.put(self.name())
        self.nest = loc.nest
        self.index = loc.index

    def eval(self, env):
        if self.index == NameEx.UNKNOWN:
            return env.get(self.name())
        else:
            return env.get(self.nest, self.index)

    def eval_for_assign(self, env, value):
        if self.index == NameEx.UNKNOWN:
            env.put(self.name(), value)
        else:
            env.put(self.nest, self.index, value)

@reviser
class BinaryEx2(basic_evaluator.BinaryEx):
    def __init__(self, list_of_astree):
        super(BinaryEx2, self).__init__(list_of_astree)

    def lookup(self, syms):
        left = self.left()
        if self.operator() == '=':
            if isinstance(left, literal.Name):
                left.lookup_for_assign(syms)
                self.right().lookup(syms)
                return

        left.lookup(syms)
        self.right().lookup(syms)

    def compute_assign(self, env, rvalue):
        l = self.left()
        if isinstance(l, literal.Name):
            l.eval_for_assign(env, rvalue)
            return rvalue
        else:
            return super(BinaryEx2, self).compute_assign(env, rvalue)




        


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
