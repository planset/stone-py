# -*- coding: utf-8 -*-

from . import func_parser
from . import mytoken
from .myast import cls, literal, fun

import parser

rule = parser.Parser.rule

class ArrayParser(func_parser.FuncParser):
    def __init__(self):
        super(ArrayParser, self).__init__()
        
        self.__make_rule()
        self.reserved.append(']')
        self.primary.insert_choice(rule().sep('[') \
                .maybe(self.elements).sep(']'))
        self.postfix.insert_choice(rule(fun.ArrayRef) \
                .sep('[').ast(self.expr).sep(']'))


    def __make_rule(self):
        self.elements = rule(literal.ArrayLiteral) \
                            .ast(self.expr) \
                            .repeat(rule().sep(',').ast(self.expr))
