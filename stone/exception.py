#!/usr/bin/env python
# -*- coding: utf-8 -*-


class IndexOutOfBoundsException(IndexError):
    def __init__(self, message):
        super(IndexOutOfBoundsException, self).__init__(message)

class RuntimeException(RuntimeError):
    def __init__(self, message):
        super(RuntimeException, self).__init__(message)

class IOException(IOError):
    def __init__(self, message):
        super(IOException, self).__init__(message)

class StoneException(RuntimeException):
    """class documentation"""
    def __init__(self, message, astree=None):
        if astree:
            message += ' ' + astree.location()
        super(StoneException, self).__init__(message)

class IllegalArgumentException(Exception):
    pass
    
class NumberFormatException(Exception):
    def __init__(self, message):
        super(NumberFormatException, self).__init__(message)
        
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
