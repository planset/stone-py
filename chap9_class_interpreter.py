#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stone import class_parser

from chap6_basic_interpreter import BasicInterpreter

from chap7 import nestedenv
from chap8 import natives
from chap9 import class_evaluator

class ClassInterpreter(BasicInterpreter):
    def testcode(self):
        return """
class A {
    value = 1
    name = "A"
    def mynameis() {
        this.name
    }
}
class B extends A {
    value = 2
    name = "B"
}

a = A.new
a.value
a.name
a.mynameis()

b = B.new
b.value
b.name
b.mynameis()

"""

    def main(self):
        self.run(class_parser.ClassParser(),
                 natives.Natives().environment(nestedenv.NestedEnv()))

if __name__ == '__main__':
    ClassInterpreter().main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

