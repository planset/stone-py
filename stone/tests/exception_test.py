# -*- coding: utf-8 -*-

from stone.myast import ast
from stone import mytoken
from stone import exception as ext
import unittest

class StoneExceptionTet(unittest.TestCase):
    def test_init(self):
        e = ext.StoneException('message')
        self.assertEqual('message', e.message)

    def test_init_two_args(self):
        t = mytoken.Token(1)
        e = ext.StoneException('message', ast.ASTList([ast.ASTLeaf(t)]))
        self.assertEqual('message at line 1', e.message)

if __name__ == '__main__':
    unittest.main() 

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
