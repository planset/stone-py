#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import only to patch original classes
from stone import basic_parser, lexer, mytoken
from stone.myast import statement as stmt
from chap6 import basic_env

from chap6 import basic_evaluator

import tempfile

f = tempfile.TemporaryFile()
f.write("""
sum = 0
i = 1
while i < 10 {
    sum = sum + i
    i = i + 1
}
sum
if sum == 45 {
    hoge = 10
}
""")
f.seek(0)

l = lexer.Lexer(f)
bp = basic_parser.BasicParser()
env = basic_env.BasicEnv()
while l.peek(0) != mytoken.Token.EOF:
    t = bp.parse(l)
    if not isinstance(t, stmt.NullStmnt):
        r = t.eval(env)
        print '=>' + str(r)

f.close()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
