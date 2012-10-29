# -*- coding: utf-8 -*-

from . import basic_parser
from .myast import fun, statement as stmnt

import parser

rule = parser.Parser.rule

class FuncParser(basic_parser.BasicParser):
    def __init__(self):
        super(FuncParser, self).__init__()
        
        self.__make_rule()
        self.reserved.append(")")
        self.primary.repeat(self.postfix)
        self.simple.option(self.args)
        self.program.insert_choice(self._def)

    def __make_rule(self):
        self.param = rule().identifier(reserved=self.reserved)
        self.params = rule(fun.ParameterList) \
                        .ast(self.param).repeat(
                            rule().sep(",").ast(self.param))

        self.param_list = rule().sep("(") \
                                .maybe(self.params).sep(")")
        self._def = rule(stmnt.DefStmnt) \
                        .sep("def").identifier(reserved=self.reserved) \
                        .ast(self.param_list).ast(self.block)
        self.args = rule(fun.Arguments) \
                        .ast(self.expr).repeat(
                            rule().sep(",").ast(self.expr))
        self.postfix = rule().sep("(").maybe(self.args).sep(")")









# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
