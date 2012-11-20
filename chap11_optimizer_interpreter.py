#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone import lexer, mytoken
from stone.myast import statement as stmt
from chap6_basic_interpreter import BasicInterpreter

from chap8 import natives

from stone import closure_parser
from chap11 import resizable_array_env

from chap8 import native_evaluator
from chap11 import env_optimizer


class EnvOptInterpreter(BasicInterpreter):
    def testcode(self):
        return """
def fib (n) {
    if n < 2 {
        n
    } else {
        fib(n - 1) + fib(n - 2)
    }
}
t = current_time()
fib 10
print current_time() - t + " msec"
"""

    def main(self):
        self.run(closure_parser.ClosureParser(),
                 natives.Natives().environment(
                     resizable_array_env.ResizableArrayEnv()))

    def run(self, bp, env):
        f = self._make_temporary_file()
        try:
            l = lexer.Lexer(f)
            while l.peek(0) != mytoken.Token.EOF:
                t = bp.parse(l)
                if not isinstance(t, stmt.NullStmnt):
                    t.lookup(env.symbols())
                    r = t.eval(env)
                    print '=>' + str(r)
        finally:
            f.close()

if __name__ == '__main__':
    EnvOptInterpreter().main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

