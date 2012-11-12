#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import ast

class ParameterList(ast.ASTList):
    def __init__(self, list_of_astree):
        super(ParameterList, self).__init__(list_of_astree)

    def name(self, i):
        return self.child(i).token().get_text()

    def size(self):
        return self.num_children()

class Postfix(ast.ASTList):
    def __init__(self, list_of_astree):
        super(Postfix, self).__init__(list_of_astree)

class Fun(ast.ASTList):
    def __init__(self, list_of_astree):
        super(Fun, self).__init__(list_of_astree)

    def parameters(self):
        return self.child(0)

    def body(self):
        return self.child(1)

    def to_string(self):
        return "(fun {} {})".format(self.parameters(), self.body())

class Arguments(Postfix):
    def __init__(self, list_of_astree):
        super(Arguments, self).__init__(list_of_astree)

    def size(self):
        return self.num_children()

class ArrayRef(Postfix):
    def __init__(self, list_of_astree):
        super(ArrayRef, self).__init__(list_of_astree)

    def index(self):
        return self.child(0)

    def to_string(self):
        return '[{}]'.format(self.index())


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
