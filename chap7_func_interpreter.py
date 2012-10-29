#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone import func_parser

from chap6_basic_interpreter import BasicInterpreter

from chap7 import nestedenv
from chap7 import function_evaluator

class FuncInterpreter(BasicInterpreter):
    def testcode(self):
        return """
def fib (n) {
    if n < 2 {
        n
    } else {
        fib(n - 1) + fib(n - 2)
    }
}
fib(10)
"""

    def main(self):
        self.run(func_parser.FuncParser(),
                 nestedenv.NestedEnv())

if __name__ == '__main__':
    FuncInterpreter().main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
