# -*- coding: utf-8 -*-

class Environment(object):
    def put(self, name, value):
        raise NotImplementedError()

    def get(self, name):
        raise NotImplementedError()

class BasicEnv(Environment):
    def __init__(self):
        self.values = {}

    def put(self, name, value):
        self.values[name] = value

    def get(self, name):
        return self.values[name]

    

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
