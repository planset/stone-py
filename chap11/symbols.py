#!/usr/bin/env python
# -*- coding: utf-8 -*-



class Symbols(object):
    class Location(object):
        def __init__(self, nest, index):
            self.nest = nest
            self.index = index

    def __init__(self, outer=None):
        self.outer = outer
        self.table = {}

    def size(self):
        return len(self.table)

    def append(self, s):
        self.table.update(s.table)

    def find(self, key):
        return self.table.get(key)

    def get(self, key, nest=0):
        index = self.table.get(key)
        if index is None:
            if self.outer is None:
                return None
            else:
                return self.outer.get(key, nest + 1)
        else:
            return Symbols.Location(nest, int(index))

    def put_new(self, key):
        i = self.find(key)
        if i is None:
            return self.add(key)
        else:
            return i

    def put(self, key):
        loc = self.get(key)
        if loc is None:
            return Symbols.Location(0, self.add(key))
        else:
            return loc

    def add(self, key):
        i = len(self.table)
        self.table[key] = i
        return i


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
