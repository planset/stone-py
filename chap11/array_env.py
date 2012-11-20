#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone import exception
from chap6 import basic_env


class ArrayEnv(basic_env.Environment):
    def __init__(self, size, out):
        self.values = [None for _ in range(size)]
        self.outer = out

    def symbols(self):
        raise exception.StoneException('no symbols')

    def _get_by_name(self, name):
        self.error(name)
        return None

    def _get_by_nest_index(self, nest, index):
        if nest == 0:
            return self.values[index]
        elif self.outer is None:
            return None
        else:
            return self.outer.get(nest - 1, index)

    def get(self, *args):
        #nest=None, index=None, name=None
        if len(args) == 2:
            nest = args[0]
            index = args[1]
            return self._get_by_nest_index(nest, index)
        elif len(args) == 1:
            name = args[0]
            return self._get_by_name(name)
        else:
            raise Exception('')

    def _put_by_nest_index(self, nest, index, value):
        if nest == 0:
            self.values[index] = value
        elif self.outer is None:
            raise exception.StoneException('no outer environment')
        else:
            return self.outer.put(nest - 1, index, value)

    def _put_by_name(self, name, value):
        self.error(name)
        return None

    def put(self, *args):
        #nest=None, index=None, value=None, name=None):
        if len(args) == 3:
            nest = args[0]
            index = args[1]
            value = args[2]
            return self._put_by_nest_index(nest, index, value)
        elif len(args) == 2:
            name = args[0]
            value = args[1]
            return self._put_by_name(name, value)
        else:
            raise Exception('')

    def put_new(self, name, value):
        self.error(name)

    def where(self, name):
        self.error(name)
        return None

    def set_outer(self, e):
        self.outer = e

    def error(self, name):
        raise exception.StoneException(
                'cannot access by name: {}'.format(name))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
