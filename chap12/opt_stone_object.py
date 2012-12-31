#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone import exception

class OptStoneObject(object):
    def __init__(self, ci, size):
        self._class_info = ci
        self.fields = [None for _ in xrange(size)]

    def class_info(self):
        return self._class_info

    def _read_by_index(self, index):
        return self.fields[index]

    def _read_by_name(self, name):
        i = self._class_info.field_index(name)
        if i is not None:
            return self.fields[i]
        else:
            i = self._class_info.method_index(name)
            if i is not None:
                return self.method(i)
        raise exception.AccessException()

    def read(self, arg):
        if isinstance(arg, int):
            return self._read_by_index(arg)
        elif isinstance(arg, str):
            return self._read_by_name(arg)
        else:
            pass

    def _write_by_index(self, index, value):
        self.fields[index] = value

    def _write_by_name(self, name, value):
        i = self._class_info.field_index(name)
        if i is not None:
            raise exception.AccessException()
        else:
            self.fields[i] = value

    def write(self, arg, value):
        if isinstance(arg, int):
            return self._write_by_index(arg, value)
        elif isinstance(arg, str):
            return self._write_by_name(arg, value)
        else:
            pass

    def method(self, index):
        return self._class_info.method(self, index)



# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
    
