#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mytoken import Token
class ParseException(Exception):
    """docstring for ParseException"""

    def __init__(self, token, message=""):
        super(ParseException, self).__init__(
                "syntax error around {}. {}".format(self.location(token), message)
                )

    def location(self, token):
        """method documentation"""
        if token == Token.EOF:
            return 'the last line'
        else:
            return '\"{}\" at line {}'.format(token.get_text(), token.line_number)

import unittest

class ParseExceptionTest(unittest.TestCase):
    def test_init_(self):
        e = ParseException(Token(1))
        self.assertEqual('syntax error arround', e.message)

if __name__ == '__main__':
    unittest.main() 
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
