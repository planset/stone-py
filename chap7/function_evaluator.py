# -*- coding: utf-8 -*-

from stone.util import reviser
from stone.myast import statement, fun, expression
from stone import exception

from chap6 import basic_env
from chap6 import basic_evaluator
from chap7 import function

@reviser
class EnvEx(basic_env.Environment):
    def put_new(self, name, value):
        raise NotImplementedError()
    def where(self, name):
        raise NotImplementedError()
    def set_outer(self, env):
        raise NotImplementedError()

@reviser
class DefStmntEx(statement.DefStmnt):
    def __init__(self, list_of_astree):
        super(DefStmntEx, self).__init__(list_of_astree)

    def eval(self, env):
        env.put_new(self.name(), 
                function.Function(self.parameters(), self.body(), env))
        return self.name()

@reviser
class PrimaryEx(expression.PrimaryExpr):
    def __init__(self, list_of_astree):
        super(PrimaryEx, self).__init__(list_of_astree)

    def operand(self):
        return self.child(0)

    def postfix(self, nest):
        return self.child(self.num_children() - nest - 1)

    def has_postfix(self, nest):
        return self.num_children() - nest > 1

    def eval(self, env):
        return self.eval_sub_expr(env, 0)

    def eval_sub_expr(self, env, nest):
        if self.has_postfix(nest):
            target = self.eval_sub_expr(env, nest + 1)
            return self.postfix(nest).eval(env, target)
        else:
            return self.operand().eval(env)

@reviser
class PostfixEx(fun.Postfix):
    def __init__(self, list_of_astree):
        super(PostfixEx, self).__init__(list_of_astree)

    def eval(self, env, value):
        raise NotImplementedError()

@reviser
class ArgumentsEx(fun.Arguments):
    def __init__(self, list_of_astree):
        super(ArgumentsEx, self).__init__(list_of_astree)

    def eval(self, caller_env, value):
        if not isinstance(value, function.Function):
            raise exception.StoneException("bad function", self)
        func = value
        params = func.parameters()
        if self.size() != params.size():
            raise exception.StoneException("bad number of arguments", self)
        new_env = func.make_env()
        num = 0
        for a in self.children():
            params.eval(new_env, num, a.eval(caller_env))
            num += 1
        return func.body().eval(new_env)

@reviser
class ParamsEx(fun.ParameterList):
    def __init__(self, list_of_astree):
        super(ParamsEx, self).__init__(list_of_astree)

    def eval(self, env, index, value):
        env.put_new(self.name(index), value)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
