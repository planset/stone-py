# -*- coding: utf-8 -*-

from stone.util import reviser, super
from stone.myast import ast, literal, expression, statement
from stone import exception

#class BasicEvaluator(object):
#    def __init__(self):
#        pass

TRUE = 1
FALSE = 0

@reviser
class ASTreeEx(ast.ASTree):
    def eval(self, env):
        raise NotImplementedError()

@reviser
class ASTListEx(ast.ASTList):
    def __init__(self, list_of_astree):
        super(ASTListEx, self).__init__(list_of_astree)

    def eval(self, env):
        raise exception.StoneException("cannot eval: " + self.to_string(), self)

@reviser
class ASTLeafEx(ast.ASTLeaf):
    def __init__(self, token):
        super(ASTLeafEx, self).__init__(token)

    def eval(self, env):
        raise exception.StoneException("cannot eval: " + self.to_string(), self)

@reviser
class NumberEx(literal.NumberLiteral):
    def __init__(self, token):
        super(NumberEx, self).__init__(token)

    def eval(self, env):
        return self.value()

@reviser
class StringEx(literal.StringLiteral):
    def __init__(self, token):
        super(StringEx, self).__init__(token)

    def eval(self, env):
        return self.value()

@reviser
class NameEx(literal.Name):
    def __init__(self, token):
        super(NameEx, self).__init__(token)

    def eval(self, env):
        value = env.get(self.name())
        if value is None:
            raise exception.StoneException('undefined name: ' + self.name(), self)
        else:
            return value

@reviser
class NegativeEx(expression.NegativeExpr):
    def __init__(self, list_of_astree):
        super(NegativeEx, self).__init__(list_of_astree)

    def eval(self, env):
        v = self.operand().eval(env)
        if isinstance(v, int):
            return -v
        else:
            raise exception.StoneException('bad type for -', self)

@reviser
class BinaryEx(expression.BinaryExpr):
    def __init__(self, list_of_astree):
        super(BinaryEx, self).__init__(list_of_astree)

    def eval(self, env):
        op = self.operator()
        if op == '=':
            right = self.right().eval(env)
            return self.compute_assign(env, right)
        else:
            left = self.left().eval(env)
            right = self.right().eval(env)
            return self.compute_op(left, op, right)

    def compute_assign(self, env, rvalue):
        l = self.left()
        if isinstance(l, literal.Name):
            env.put(l.name(), rvalue)
            return rvalue
        else:
            raise expression.StoneException('bad assignment', self)

    def compute_op(self, left, op, right):
        if isinstance(left, int) and isinstance(right, int):
            return self.compute_number(left, op, right)
        else:
            if op == '+':
                return str(left) + str(right)
            elif op == '==':
                if left is None:
                    return TRUE if right else FALSE
                else:
                    return TRUE if left == right else FALSE
            else:
                raise exception.StoneException('bad type', self)

    def compute_number(self, left, op, right):
        a = int(left)
        b = int(right)
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a / b
        elif op == '%':
            return a % b
        elif op == '==':
            return TRUE if a == b else FALSE
        elif op == '>':
            return TRUE if a > b else FALSE
        elif op == '<':
            return TRUE if a < b else FALSE
        else:
            return exception.StoneException('bad operator', self)

@reviser
class BlockEx(statement.BlockStmnt):
    def __init__(self, list_of_astree):
        super(BlockEx, self).__init__(list_of_astree)

    def eval(self, env):
        result = 0
        for token in self.children():
            if not isinstance(token, statement.NullStmnt):
                result = token.eval(env)
        return result

@reviser
class IfEx(statement.IfStmnt):
    def __init__(self, list_of_astree):
        super(IfEx, self).__init__(list_of_astree)

    def eval(self, env):
        c = self.condition().eval(env)
        if isinstance(c, int) and int(c) != FALSE:
            return self.then_block().eval(env)
        else:
            b = self.else_block()
            if b is None:
                return 0
            else:
                return b.eval(env)

@reviser
class WhileEx(statement.WhileStmnt):
    def __init__(self, list_of_astree):
        super(WhileEx, self).__init__(list_of_astree)

    def eval(self, env):
        result = 0
        while True:
            c = self.condition().eval(env)
            if isinstance(c, int) and int(c) == FALSE:
                return result
            else:
                result = self.body().eval(env)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
