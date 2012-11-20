#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chap11 import array_env, symbols

class ResizableArrayEnv(array_env.ArrayEnv):
    def __init__(self):
        super(ResizableArrayEnv, self).__init__(10, None)
        self.names = symbols.Symbols()

    def symbols(self):
        return self.names

    def _get_by_name(self, name):
        i = self.names.find(name)
        if i is None:
            if self.outer is None:
                return None
            else:
                return self.outer.get(name=name)

    def _put_by_name(self, name, value):
        e = self.where(name)
        if e is None:
            e = self
        e.put_new(name, value)

    def put_new(self, name, value):
        self.assign(self.names.put_new(name), value)

    def where(self, name):
        if self.names.find(name) is not None:
            return self
        elif self.outer is None:
            return None
        else:
            return self.outer.where(name)

    def _put_by_nest_index(self, nest, index, value):
        if nest == 0:
            self.assign(index, value)
        else:
            super(ResizableArrayEnv, self) \
                    ._put_by_nest_index(nest, index, value)

    def assign(self, index, value):
        if index >= len(self.values):
            new_len = len(self.values) * 2
            if index >= new_len:
                new_len = index + 1
            self.values += [None for _ in xrange(new_len - len(self.values))]
        # array_b = Arrays.copyOf(array_a, length)
        # array_aをarray_bにlength分コピーする。lengthがarray_aの
        # サイズよりも大きい場合、超えた分はnullが入る。
        self.values[index] = value

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
