#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone import closure_parser

from chap6_basic_interpreter import BasicInterpreter

from chap7 import nestedenv
from chap8 import native_evaluator
from chap8 import natives

class NativeInterpreter(BasicInterpreter):
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
fib 15
print current_time() - t + " msec"
"""

    def main(self):
        self.run(closure_parser.ClosureParser(),
                 natives.Natives().environment(nestedenv.NestedEnv()))

if __name__ == '__main__':
    NativeInterpreter().main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

