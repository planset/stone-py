#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import nestedenv

class Function(object):
    def __init__(self, parameters, body, env):
        """constructor

        :param parameters: fun.ParameterList
        :param body: BlockStmnt
        :param env: Environment
        """
        self._parameters = parameters
        self._body = body
        self.env = env

    def parameters(self):
        return self._parameters

    def body(self):
        return self._body

    def make_env(self):
        return nestedenv.NestedEnv(self.env)

    def __str__(self):
        return "<fun:{}>".format(self.__hash__())
    
    

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
