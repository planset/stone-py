# -*- coding: utf-8 -*-

from myast import (literal as lit,
                   statement as stmnt,
                   expression as expr)
import mytoken
import util 
import parser

rule = parser.Parser.rule

class BasicParser(object):

    def __init__(self):
        self.__make_reserved()
        self.__make_operators()
        self.__make_rule()

    def __make_reserved(self):
        self.reserved = util.HashSet()
        self.reserved.append(";")
        self.reserved.append("}")
        self.reserved.append(mytoken.Token.EOL)

    def __make_operators(self):
        self.operators = parser.Operators()
        self.operators.add("=", 1, parser.Operators.RIGHT);
        self.operators.add("==", 2, parser.Operators.LEFT);
        self.operators.add(">", 2, parser.Operators.LEFT);
        self.operators.add("<", 2, parser.Operators.LEFT);
        self.operators.add("+", 3, parser.Operators.LEFT);
        self.operators.add("-", 3, parser.Operators.LEFT);
        self.operators.add("*", 4, parser.Operators.LEFT);
        self.operators.add("/", 4, parser.Operators.LEFT);
        self.operators.add("%", 4, parser.Operators.LEFT);

    def __make_rule(self):
        self.expr0 = rule()
        self.primary = rule(expr.PrimaryExpr) \
                .or_(rule().sep("(").ast(self.expr0).sep(")"),
                     rule().number(lit.NumberLiteral),
                     rule().identifier(lit.Name, self.reserved),
                     rule().string(lit.StringLiteral))

        self.factor = rule().or_(
                rule(expr.NegativeExpr).sep("-").ast(self.primary),
                self.primary)

        self.expr = self.expr0.expression(self.factor, 
                                          self.operators,
                                          expr.BinaryExpr)

        self.statement0 = rule()
        self.block = rule(stmnt.BlockStmnt) \
                .sep("{").option(self.statement0) \
                .repeat(rule().sep(";", mytoken.Token.EOL) \
                        .option(self.statement0)) \
                .sep("}")
        self.simple = rule(expr.PrimaryExpr).ast(self.expr)
        self.statement = self.statement0.or_(
                rule(stmnt.IfStmnt).sep("if").ast(self.expr).ast(self.block) \
                     .option(rule().sep("else").ast(self.block)),
                rule(stmnt.WhileStmnt).sep("while").ast(self.expr).ast(self.block),
                self.simple)
        self.program = rule().or_(self.statement, 
                                  rule(stmnt.NullStmnt)) \
                             .sep(";", mytoken.Token.EOL)


    def parse(self, lexer):
        return self.program.parse(lexer)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
