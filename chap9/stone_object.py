#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone import exception

class StoneObject(object):
    def __init__(self, e):
        self.env = e

    def to_string(self):
        return '<object:{}>'.format(self.__hash__)

    def read(self, member):
        return self.get_env(member).get(member)

    def write(self, member, value):
        self.get_env(member).put_new(member, value)

    def get_env(self, member):
        e = self.env.where(member)
        if e is not None and e == self.env:
            return e
        else:
            raise exception.AccessException()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
