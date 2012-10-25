#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from stone import basic_parser, lexer, mytoken
from stone.myast import statement as stmt
from chap6 import basic_env
from chap6 import basic_evaluator


def run_interpreter(f):
    l = lexer.Lexer(f)
    bp = basic_parser.BasicParser()
    env = basic_env.BasicEnv()
    while l.peek(0) != mytoken.Token.EOF:
        t = bp.parse(l)
        if not isinstance(t, stmt.NullStmnt):
            r = t.eval(env)
            print '=>' + str(r)

def run_from_file(filepath):
    with open(filepath, 'r') as f:
        run_interpreter(f)

def run_from_code(code):
    import tempfile
    f = None
    try:
        f = tempfile.TemporaryFile()
        f.write(code)
        f.seek(0)
        run_interpreter(f)
    finally:
        if f: f.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--code')
    parser.add_argument('filepath', nargs='?')
    args = parser.parse_args()
    if args.code is None and args.filepath is None:
        print 'error: too few arguments'
        sys.exit()
    elif args.filepath is not None:
        run_from_file(args.filepath)
    elif args.code is not None:
        run_from_code(args.code)
    

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
