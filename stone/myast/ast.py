# -*- coding: utf-8 -*-

class ASTree(object):
    def child(self, i):
        raise NotImplementedError()
    
    def num_children(self):
        raise NotImplementedError()

    def children(self):
        raise NotImplementedError()

    def location(self):
        raise NotImplementedError()

    def __iter__(self):
        return self.children()

    def next(self):
        return self.children().next()

    def name(self):
        return 'NotImplemented'

    def to_string(self):
        return self.name()

    def __str__(self):
        return self.to_string()


class ASTLeaf(ASTree):
    empty = []

    def __init__(self, token):
        self.token = token

    def child(self, i):
        raise IndexError()

    def num_children(self):
        return 0

    def children(self):
        return iter(self.empty)

    def location(self):
        return 'at line {}'.format(self.token.line_number)

    def name(self):
        if self.token:
            return self.token.get_text()
        return 'NotImplemented'

    def token(self):
        return self.token


class ASTList(ASTree):
    def __init__(self, list_of_astree):
        self.astree_list = list_of_astree

    def child(self, i):
        return self.astree_list[i]

    def children(self):
        return self.astree_list

    def num_children(self):
        return len(self.astree_list)

    def to_string(self):
        builder = []
        builder.append('(') 
        sep = ''
        for t in self.children():
            builder.append(sep)
            sep = ' '
            builder.append(t.to_string())
        builder.append(')')
        return ''.join(builder)

    def location(self):
        for t in self.children():
            s = t.location()
            if s:
                return s
        return None


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

