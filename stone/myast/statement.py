# -*- coding: utf-8 -*-

from . import ast


class BlockStmnt(ast.ASTList):
    def __init__(self, list_of_astree):
        super(BlockStmnt, self).__init__(list_of_astree)

class IfStmnt(ast.ASTList):
    def __init__(self, list_of_astree):
        super(IfStmnt, self).__init__(list_of_astree)

    def condition(self):
        return self.child(0)

    def then_block(self):
        return self.child(1)

    def else_block(self):
        return self.child(2) if self.num_children() > 2 else None

    def to_string(self):
        return '(if {} {} else {} )'.format(
                self.condition(),
                self.then_block(),
                self.else_block())

class WhileStmnt(ast.ASTList):
    def __init__(self, list_of_astree):
        super(WhileStmnt, self).__init__(list_of_astree)

    def condition(self):
        return self.child(0)

    def body(self):
        return self.child(1)

    def to_string(self):
        return '(while {} {} )'.format(
                self.condition(),
                self.body())

class NullStmnt(ast.ASTList):
    def __init__(self, list_of_astree):
        super(NullStmnt, self).__init__(list_of_astree)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
