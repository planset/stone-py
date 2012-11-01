# -*- coding: utf-8 -*-

from . import func_parser
from .myast import fun

import parser

rule = parser.Parser.rule

class ClosureParser(func_parser.FuncParser):
    def __init__(self):
        super(ClosureParser, self).__init__()

        self.primary.insert_choice(rule(fun.Fun) \
                .sep("fun").ast(self.param_list).ast(self.block))



