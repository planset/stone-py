# -*- coding: utf-8 -*-

from . import ast

class BinaryExpr(ast.ASTList):
    def __init__(self, list_of_astree):
        super(BinaryExpr, self).__init__(list_of_astree)

    def left(self):
        return self.child(0)
    
    def operator(self):
        return self.child(1).token().get_text()

    def right(self):
        return self.child(2)

class NegativeExpr(ast.ASTList):
    def __init__(self, list_of_astree):
        super(NegativeExpr, self).__init__(list_of_astree)

    def operand(self):
        return self.child(0)

    def to_string(self):
        return '-' + self.operand()

class PrimaryExpr(ast.ASTList):
    def __init__(self, list_of_astree):
        super(PrimaryExpr, self).__init__(list_of_astree)

    @classmethod
    def create(cls, list_of_astree):
        return list_of_astree[0] if len(list_of_astree) == 1 else PrimaryExpr(list_of_astree)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
