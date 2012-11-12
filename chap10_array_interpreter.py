#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone import array_parser

from chap6_basic_interpreter import BasicInterpreter

from chap7 import nestedenv
from chap8 import natives

from chap7 import closure_evaluator
from chap8 import native_evaluator
from chap9 import class_evaluator
from chap10 import array_evaluator

class ArrayInterpreter(BasicInterpreter):
    def testcode(self):
        return """
a = [2, 3, 4]
print a[1]
a[1] = "three"
print "a[1]: " + a[1]
b = [["one", 1], ["two", 2]]
print b[1][0] + ": " + b[1][1]
"""

    def main(self):
        self.run(array_parser.ArrayParser(),
                 natives.Natives().environment(nestedenv.NestedEnv()))

if __name__ == '__main__':
    ArrayInterpreter().main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


