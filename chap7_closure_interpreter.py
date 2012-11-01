#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone import closure_parser

from chap6_basic_interpreter import BasicInterpreter

from chap7 import nestedenv
from chap7 import closure_evaluator

class ClosureInterpreter(BasicInterpreter):
    def testcode(self):
        return """
inc = fun (x) { x + 1 }
inc(3)
def counter (c) {
    fun () { c = c + 1 }
}
c1 = counter(0)
c2 = counter(0)
c1()
c1()
c2()
"""

    def main(self):
        self.run(closure_parser.ClosureParser(),
                 nestedenv.NestedEnv())

if __name__ == '__main__':
    ClosureInterpreter().main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

