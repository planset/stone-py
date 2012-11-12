#!/usr/bin/env python
# -*- coding: utf-8 -*-
from stone.util import reviser, super
from stone import exception
from stone.myast import cls, expression

from chap6 import basic_evaluator
from chap7 import function_evaluator
from chap7 import nestedenv
from chap9 import stone_object

from . import class_info

@reviser
class ClassStmntEx(cls.ClassStmnt):
    def __init__(self, list_of_astree):
        super(ClassStmntEx, self).__init__(list_of_astree)

    def eval(self, env):
        ci = class_info.ClassInfo(self, env)
        env.put(self.name(), ci)
        return self.name()

@reviser
class ClassBodyEx(cls.ClassBody):
    def __init__(self, list_of_astree):
        super(ClassBodyEx, self).__init__(list_of_astree)

    def eval(self, env):
        for t in self.children():
            t.eval(env)
        return None

@reviser
class DotEx(cls.Dot):
    def __init__(self, list_of_astree):
        super(DotEx, self).__init__(list_of_astree)

    def eval(self, env, value):
        member = self.name()
        if isinstance(value, class_info.ClassInfo):
            if member == 'new':
                ci = value
                e = nestedenv.NestedEnv(ci.environment)
                so = stone_object.StoneObject(e)
                e.put_new('this', so)
                self.init_object(ci, e)
                return so
        elif isinstance(value, stone_object.StoneObject):
            try:
                return value.read(member)
            except exception.AccessException as e:
                pass
        raise exception.StoneException('bad member access: ' + member, self)

    def init_object(self, ci, env):
        if ci.super_class() is not None:
            self.init_object(ci.super_class(), env)
        ci.body().eval(env)


@reviser
class AssignEx(basic_evaluator.BinaryEx):
    def __init__(self, list_of_astree):
        super(AssignEx, self).__init__(list_of_astree)

    def compute_assign(self, env, rvalue):
        le = self.left()
        if isinstance(le, expression.PrimaryExpr):
            p = le
            if p.has_postfix(0) and isinstance(p.postfix(0), cls.Dot):
                t = le.eval_sub_expr(env, 1)
                if isinstance(t, stone_object.StoneObject):
                    return self.set_field(t, p.postfix(0), rvalue)
        return super(AssignEx, self).compute_assign(env, rvalue)

    def set_field(self, obj, expr, rvalue):
        name = expr.name()
        try:
            obj.write(name, rvalue)
            return rvalue
        except exception.AccessException:
            raise exception.StoneException('bad member access {}: {}' \
                    .format(self.location(), self.name()))



