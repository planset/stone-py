# -*- coding: utf-8 -*-

from . import closure_parser
from . import mytoken
from .myast import cls

import parser

rule = parser.Parser.rule

class ClassParser(closure_parser.ClosureParser):
    def __init__(self):
        super(ClassParser, self).__init__()
        
        self.__make_rule()
        self.postfix.insert_choice(
                rule(cls.Dot).sep(".").identifier(reserved=self.reserved))
        self.program.insert_choice(self.defclass)

    def __make_rule(self):
        self.member = rule().or_(self._def, self.simple)
        self.class_body = rule(cls.ClassBody) \
                            .sep("{").option(self.member) \
                            .repeat(rule().sep(";", mytoken.Token.EOL) \
                                          .option(self.member)) \
                            .sep("}")
        self.defclass = rule(cls.ClassStmnt) \
                            .sep("class").identifier(reserved=self.reserved) \
                            .option(rule().sep("extends") \
                                          .identifier(reserved=self.reserved)) \
                            .ast(self.class_body)




