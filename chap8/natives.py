#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone import exception
from chap8 import native_function
import datetime


class Natives(object):
    start_time = datetime.datetime.now()

    def environment(self, env):
        self._append_natives(env)
        return env

    def _append_natives(self, env):
        self._append(env, "print", Natives, "_print", object)
        self._append(env, "read", Natives, "_read")
        self._append(env, "length", Natives, "_length", str)
        self._append(env, "to_int", Natives, "_to_int", object)
        self._append(env, "current_time", Natives, "_current_time")
    
    def _append(self, env, name, cls, method_name, class_of_params=None):
        m = None
        try:
            m = cls.__dict__[method_name].__func__
        except:
            raise exception.StoneException("cannot find a native function: {}" \
                                            .format(method_name))
        env.put(name, native_function.NativeFunction(cls.__name__ + '.' + method_name, m))

    @staticmethod
    def _print(obj):
        print obj
        return 0

    @staticmethod
    def _read():
        return raw_input()

    @staticmethod
    def _length(s):
        return len(s)

    @staticmethod
    def _to_int(value):
        if isinstance(value, str):
            return int(value)
        elif isinstance(value , int):
            return value
        else:
            raise exception.NumberFormatException(str(value))

    @staticmethod
    def _current_time():
        td = datetime.datetime.now() - Natives.start_time
        ms = int(td.total_seconds() * 1000)
        return ms


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
