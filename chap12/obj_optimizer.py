#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone.myast import cls, statement, expression
from stone.util import reviser, super
from stone import exception

from chap6 import basic_evaluator
from chap11 import env_optimizer, symbols, array_env
from chap12 import symbol_this, opt_class_info, member_symbols, opt_stone_object


@reviser
class ClassStmntEx(cls.ClassStmnt):
    def __init__(self, list_of_astree):
        super(ClassStmntEx, self).__init__(list_of_astree)

    def lookup(self, syms):
        pass

    def eval(self, env):
        method_names = member_symbols.MemberSymbols(
                env.symbols(), member_symbols.MemberSymbols.METHOD)
        field_names = member_symbols.MemberSymbols(
                method_names, member_symbols.MemberSymbols.FIELD)
        ci = opt_class_info.OptClassInfo(self, env, 
                method_names, field_names)
        env.put(self.name(), ci)
        methods = []
        if ci.super_class():
            ci.super_class().copy_to(field_names, method_names, methods)
        new_syms = symbol_this.SymbolThis(field_names)
        self.body().lookup(new_syms, method_names, field_names, methods)
        ci.set_methods(methods)
        return self.name()

@reviser
class ClassBodyEx(cls.ClassBody):
    def __init__(self, list_of_astree):
        super(ClassBodyEx, self).__init__(list_of_astree)

    def eval(self, env):
        for t in self.children():
            if not isinstance(t, statement.DefStmnt):
                t.eval(env)
        return None

    def lookup(self, syms, method_names, field_names, methods):
        for t in self.children():
            if isinstance(t, statement.DefStmnt):
                _def = t
                old_size = method_names.size()
                i = method_names.put_new(_def.name())
                if i >= old_size:
                    methods.append(_def)
                else:
                    methods[i] = _def
                _def.lookup_as_method(field_names)
            else:
                t.lookup(syms)

@reviser
class DefStmntEx2(env_optimizer.DefStmntEx):
    def __init__(self, list_of_astree):
        super(DefStmntEx2, self).__init__(list_of_astree)

    def locals(self):
        return self.size

    def lookup_as_method(self, syms):
        new_syms = symbols.Symbols(syms)
        new_syms.put_new(symbol_this.SymbolThis.NAME)
        self.parameters().lookup(new_syms)
        self.body().lookup(new_syms)
        self.size = new_syms.size()


@reviser
class DotEx(cls.Dot):
    def __init__(self, list_of_astree):
        super(DotEx, self).__init__(list_of_astree)

    def eval(self, env, value):
        member = self.name()
        if isinstance(value, opt_class_info.OptClassInfo):
            if member == 'new':
                ci = value
                new_env = array_env.ArrayEnv(1, ci.environment())
                so = opt_stone_object.OptStoneObject(ci, ci.size())
                new_env.put(0, 0, so)
                self.init_object(ci, so, new_env)
                return so
        elif isinstance(value, opt_stone_object.OptStoneObject):
            try:
                return value.read(member)
            except:
                pass
        raise exception.StoneException('bad member access: {}'.format(member), self)

    def init_object(self, ci, obj, env):
        if ci.super_class():
            self.init_object(ci.super_class(), obj, env)
        ci.body().eval(env)

@reviser
class NameEx2(env_optimizer.NameEx):
    def __init__(self, t):
        super(NameEx2, self).__init__(t)
    
    def eval(self, env):
        if self.index == env_optimizer.NameEx.UNKNOWN:
            return env.get(self.name())
        elif self.nest == member_symbols.MemberSymbols.FIELD:
            return self.get_this(env).read(self.index)
        elif self.nest == member_symbols.MemberSymbols.METHOD:
            return self.get_this(env).method(self.index)
        else:
            return env.get(self.nest, self.index)

    def eval_for_assign(self, env, value):
        if self.index == env_optimizer.NameEx.UNKNOWN:
            env.put(self.name(), value)
        elif self.nest == member_symbols.MemberSymbols.FIELD:
            self.get_this(env).write(self.index, value)
        elif self.nest == member_symbols.MemberSymbols.METHOD:
            raise exception.StoneException(
                    'cannnot update a method: {}'.format(self.name()), self)
        else:
            env.put(self.nest, self.index, value)

    def get_this(self, env):
        return env.get(0, 0)


#class AssignEx(basic_evaluator.BinaryEx):

@reviser
class AssignEx(env_optimizer.BinaryEx2):
    def __init__(self, list_of_astree):
        super(AssignEx, self).__init__(list_of_astree)

    def compute_assign(self, env, rvalue):
        le = self.left()
        if isinstance(le, expression.PrimaryExpr):
            p = le
            if p.has_postfix(0) and isinstance(p.postfix(0), cls.Dot):
                t = le.eval_sub_expr(env, 1)
                if isinstance(t, opt_stone_object.OptStoneObject):
                    return self.set_field(t, p.postfix(0), rvalue)
        return super(AssignEx, self).compute_assign(env, rvalue)
    
    def set_field(self, obj, expr, rvalue):
        name = expr.name()
        try:
            obj.write(name, rvalue)
            return rvalue
        except:
            raise exception.StoneException('bad member access: {}'.format(name), self)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
