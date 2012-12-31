#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import ast, fun

class ClassBody(ast.ASTList):
    def __init__(self, list_of_astree):
        super(ClassBody, self).__init__(list_of_astree)

class ClassStmnt(ast.ASTList):
    def __init__(self, list_of_astree):
        super(ClassStmnt, self).__init__(list_of_astree)

    def name(self):
        return self.child(0).token().get_text()

    def super_class(self):
        if self.num_children() < 3:
            return None
        else:
            return self.child(1).token().get_text()

    def body(self):
        return self.child(self.num_children() - 1)

    def to_string(self):
        parent = self.super_class()
        if parent is None:
            parent = "*"
        return "(class {} {} {})" \
                .format(self.name(), self.parent(), self.body())


class Dot(fun.Postfix):
    class_info = None
    is_field = False
    index = 0

    def __init__(self, list_of_astree):
        super(Dot, self).__init__(list_of_astree)

    def name(self):
        return self.child(0).token().get_text()

    def to_string(self):
        return "." + self.name()


