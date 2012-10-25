# -*- coding: utf-8 -*-

from myast import ast
import mytoken 
import exception
import parse_exception
import util

class Parser(object):
    def __init__(self, class_type=None, parser=None):
        if parser and isinstance(parser, Parser):
            self.elements = parser.elements
            self.factory = parser.factory
        else:
            self.reset(class_type)
    
    def reset(self, *args):
        self.elements = []
        if len(args) > 0:
            self.factory = Factory.get_for_astlist(args[0])
        return self

    def parse(self, lexer):
        results = []
        for e in self.elements:
            e.parse(lexer, results)
        return self.factory.make(results)

    def match(self, lexer):
        if len(self.elements) == 0:
            return True
        else:
            e = self.elements[0]
            return e.match(lexer)

    @staticmethod
    def rule(class_type=None):
        return Parser(class_type=class_type)

    def number(self, class_type=None):
        self.elements.append(NumToken(class_type))
        return self

    def identifier(self, class_type=None, reserved=None):
        self.elements.append(IdToken(class_type, reserved))
        return self

    def string(self, class_type=None):
        self.elements.append(StrToken(class_type))
        return self

    def token(self, *pat):
        self.elements.append(Leaf(pat))
        return self

    def sep(self, *pat):
        self.elements.append(Skip(pat))
        return self

    def ast(self, p):
        self.elements.append(Tree(p))
        return self

    def or_(self, *p):
        self.elements.append(OrTree(p))
        return self

    def maybe(self, p):
        p2 = Parser(parser=p)
        p2.reset()
        self.elements.append(OrTree([p, p2]))
        return self

    def option(self, p):
        self.elements.append(Repeat(p, True))
        return self

    def repeat(self, p):
        self.elements.append(Repeat(p, False))
        return self

    def expression(self, subexp, operators, class_type=None):
        self.elements.append(Expr(class_type, subexp, operators))
        return self

    def insert_choice(self, p):
        e = self.elements[0]
        if isinstance(e, OrTree):
            e.insert(p)
        else:
            otherwise = Parser(parser=self)
            self.reset(None)
            self.or_(p, otherwise)
        return self


class Element(object):
    def parse(self, lexer, results):
        raise NotImplementedError()

    def match(self, lexer):
        raise NotImplementedError()

class Tree(Element):
    def __init__(self, parser):
        self.parser = parser

    def parse(self, lexer, results):
        results.append(self.parser.parse(lexer))

    def match(self, lexer):
        return self.parser.match(lexer)

class OrTree(Element):
    def __init__(self, parsers):
        self.parsers = parsers

    def parse(self, lexer, results):
        parser = self.choose(lexer)
        if parser is None:
            raise exception.ParseException(lexer.peek(0))
        else:
            results.append(parser.parse(lexer))

    def match(self, lexer):
        return self.choose(lexer) is not None

    def choose(self, lexer):
        for parser in self.parsers:
            if parser.match(lexer):
                return parser
        return None

    def insert(self, parser):
        self.parsers.insert(0, parser)


class Repeat(Element):
    def __init__(self, parser, only_once):
        self.parser = parser
        self.only_once = only_once

    def parse(self, lexer, results):
        while self.parser.match(lexer):
            t = self.parser.parse(lexer)
            if not isinstance(t, ast.ASTList) or t.num_children() > 0:
                results.append(t)
            if self.only_once:
                break

    def match(self, lexer):
        return self.parser.match(lexer)


class AToken(Element):
    def __init__(self, class_type):
        if class_type is None:
            class_type = ast.ASTLeaf
        self.factory = Factory.get(class_type, mytoken.Token) 

    def parse(self, lexer, results):
        token = lexer.read()
        if self.test(token):
            leaf = self.factory.make(token)
            results.append(leaf)
        else:
            raise exception.ParseException(token) 

    def match(self, lexer):
        return self.test(lexer.peek(0))

    def test(self, token):
        raise NotImplementedError()

class IdToken(AToken):
    def __init__(self, class_type, reserved):
        super(IdToken, self).__init__(class_type)
        if reserved is not None:
            self.reserved = reserved
        else:
            self.reserved = util.HashSet()
    
    def test(self, token):
        return token.is_identifier() \
                and not self.reserved.contains(token.get_text())

class NumToken(AToken):
    def __init__(self, class_type):
        super(NumToken, self).__init__(class_type)

    def test(self, token):
        return token.is_number()

class StrToken(AToken):
    def __init__(self, class_type):
        super(StrToken, self).__init__(class_type)

    def test(self, token):
        return token.is_string()

class Leaf(Element):
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self, lexer, results):
        token = lexer.read()
        if token.is_identifier():
            for tmp_token in self.tokens:
                if tmp_token == token.get_text():
                    self.find(results, token)
                    return
        if len(self.tokens) > 0:
            raise parse_exception.ParseException(token, self.tokens[0] + " expected.")
        else:
            raise parse_exception.ParseException(token)

    def find(self, results, token):
        results.append(ast.ASTLeaf(token))

    def match(self, lexer):
        token = lexer.peek(0)
        if token.is_identifier():
            for tmp_token in self.tokens:
                if tmp_token == token.get_text():
                    return True
        return False

class Skip(Leaf):
    def __init__(self, tokens):
        super(Skip, self).__init__(tokens)

    def find(self, results, token):
        pass

class Precedence(object):
    def __init__(self, value, is_left_associative):
        self.value = value
        self.is_left_associative = is_left_associative 

class Operators(dict):
    LEFT = True
    RIGHT = False
    def add(self, name, prec, is_left_associative):
        self[name] = Precedence(prec, is_left_associative)

class Expr(Element):
    def __init__(self, class_type, expression_parser, operators):
        if not issubclass(class_type, ast.ASTree):
            raise Exception('class_type {} is not subclass of ast.ASTree'.format(class_type))
        self.factory = Factory.get_for_astlist(class_type)
        self.operators = operators
        self.factor = expression_parser

    def parse(self, lexer, astree_list):
        right = self.factor.parse(lexer)
        prec = self._next_operator(lexer)
        while not prec is None:
            right = self._do_shift(lexer, right, prec.value)
            prec = self._next_operator(lexer)
        astree_list.append(right)

    def _do_shift(self, lexer, left, prec):
        l = [left, ast.ASTLeaf(lexer.read())]
        right = self.factor.parse(lexer)
        next_op = self._next_operator(lexer)
        while next_op is not None and Expr._right_is_expr(prec, next_op):
            right = self._do_shift(lexer, right, next_op.value)
            next_op = self._next_operator(lexer)
        l.append(right)
        return self.factory.make(l)

    def _next_operator(self, lexer):
        token = lexer.peek(0)
        if token.is_identifier():
            return self.operators.get(token.get_text())
        else:
            return None

    @staticmethod
    def _right_is_expr(prec, next_prec):
        if next_prec.is_left_associative:
            return prec < next_prec.value
        else:
            return prec <= next_prec.value

    def match(self, lexer):
        return self.factor.match(lexer)

FACTORY_NAME = 'create'
class Factory(object):
    def make0(self, arg):
        raise NotImplementedError

    def make(self, arg):
        try:
            return self.make0(arg)
        except exception.IllegalArgumentException as e1:
            raise e1
        except Exception as e:
            raise e

    @staticmethod
    def get_for_astlist(class_type):
        f = Factory.get(class_type, list)
        if f is None:
            f = Factory()
            def _make0(arg):
                results = arg
                if len(results) == 1:
                    return results[0]
                else:
                    return ast.ASTList(results)
            f.make0 = _make0
        return f

    @staticmethod
    def get(class_type, arg_type):
        if class_type is None:
            return None
        
        try:
            # createの引数がargTypeで決められないので、create実装側でoverloadっぽくする必要あるかも。
            m = class_type.__dict__[FACTORY_NAME].__func__
            f = Factory()
            def _make_by_create(arg):
                return m(class_type, arg)
                # return (ASTree)m.invoke(null, arg);
                # invoke(null,arg) でJavaでいうクラスメソッドの呼び出しのはず？
                # return m(None, arg)だとclsがNoneになってしまうので、
                # return m(class_type, arg)のほうが適切かなぁ?
                # それとも、@staticmethodにしてreturn m(arg)でいいかなぁ。
            f.make0 = _make_by_create
            return f
        except TypeError as e:
            pass
        except KeyError as e:
            pass

        try:
            f = Factory()
            def _make_by_class(arg):
                return class_type(arg)
            f.make0 = _make_by_class
            return f
        except TypeError as e:
            print 'error = ', e
            raise exception.RuntimeError(e)





# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
