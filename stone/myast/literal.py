# -*- coding: utf-8 -*-

from . import ast

class NumberLiteral(ast.ASTLeaf):
    def __init__(self, token):
        super(NumberLiteral, self).__init__(token)

    def value(self):
        return self.token.get_number()

class Name(ast.ASTLeaf):
    def __init__(self, token):
        super(Name, self).__init__(token)

    def name(self):
        return self.token.get_text()

class BinaryExpr(ast.ASTList):
    def __init__(self, list_of_astree):
        super(BinaryExpr, self).__init__(list_of_astree)

    def left(self):
        return self.child(0)

    def operator(self):
        return self.child(1).token.get_text()

class StringLiteral(ast.ASTLeaf):
    def __init__(self, token):
        super(StringLiteral, self).__init__(token)

    def value(self):
        return self.token.get_text()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
