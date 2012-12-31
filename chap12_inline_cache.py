#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chap8 import natives

from stone import class_parser
from chap11 import resizable_array_env

from chap11_optimizer_interpreter import EnvOptInterpreter

from chap8 import native_evaluator
from chap12 import inline_cache

class ObjOptInterpreter(EnvOptInterpreter):
    def testcode(self):
        return """
class Fib {
    fib0 = 0
    fib1 = 1
    def fib (n) {
        if n == 0 {
            fib0
        } else {
            if n == 1 {
                this.fib1
            } else {
                fib(n - 1) + this.fib(n - 2)
            }
        }
    }
}
t = current_time()
f = Fib.new
f.fib 10
print current_time() - t + " msec"
"""

    def main(self):
        self.run(class_parser.ClassParser(),
                 natives.Natives().environment(
                     resizable_array_env.ResizableArrayEnv()))


if __name__ == '__main__':
    ObjOptInterpreter().main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

