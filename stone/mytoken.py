#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone_exception import StoneException

class EOFToken(object):
    pass

class Token(object):
    EOF = EOFToken()
    EOL = r'\n'

    _line_number = 0
    def line_number():
        doc = "The line_number property."
        def fget(self):
            return self._line_number
        def fset(self, value):
            self._line_number = value

    def __init__(self, line):
        """method documentation"""
        self.line_number = line

    def is_identifier(self):
        """method documentation"""
        return False

    def is_number(self):
        """method documentation"""
        return False

    def is_string(self):
        """method documentation"""
        return False

    def get_number(self):
        """method documentation"""
        raise StoneException("not number token")

    def get_text(self):
        """method documentation"""
        return ''

        

import unittest
class TokenTest(unittest.TestCase):
    def test_init(self):
        t = Token(1)
        self.assertEqual(1, t.line_number)
        self.assertIsInstance(t.EOF, EOFToken)

if __name__ == '__main__':
    unittest.main()


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
