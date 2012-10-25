# -*- coding: utf-8 -*-

import re
import string

from . import mytoken
from . import reader
from . import exception
from . import parse_exception


class Lexer(object):
    """class Lexer"""
    regex_pat = r"""
              \s*((/.*)|([0-9]+)| 
              (\"(\\\"|\\\\|\\n|[^\"])*\")
              |[A-Z_a-z][A-Z_a-z0-9]*|==|
              <=|>=|&&|\|\||[{punct}])?""".format(
                      punct=re.escape(string.punctuation)
                      )
    queue = []
    has_more = False
    reader = None
    
    def __init__(self, f):
        """class Lexer
        
        :param f: file"""
        self.pattern = re.compile(self.regex_pat, re.IGNORECASE | re.VERBOSE | re.MULTILINE)
        self.has_more = True
        self.reader = reader.LineNumberReader(f)

    def read(self):
        if self.fill_queue(0):
            return self.queue.pop(0)
        else:
            return mytoken.Token.EOF

    def peek(self, i):
        if self.fill_queue(i):
            return self.queue[i]
        else:
            return mytoken.Token.EOF

    def fill_queue(self, i):
        while i >= len(self.queue):
            if self.has_more:
                self.readline()
            else:
                return False
        return True

    def readline(self):
        try:
            line = self.reader.readline()
        except exception.IOException, e:
            raise parse_exception.ParseException(e)
        if line == '':
            self.has_more = False
            return
        line_no = self.reader.get_line_number()
        #matcher = self.pattern.search(line) #python match is complete match from top of line
        # useTransparentBounds 先読みとか
        # useAnchoringBouds ^ $ 
        #matcher.useTransparentBounds(true).useAnchoringBounds(false)
        # pos = 0
        # end_pos = len(line)
        # while pos < end_pos:
        #     matcher.region(pos,  end_pos)
        #     if matcher.lookingAt():
        #         self.add_token(line_no,  matcher)
        #         pos = matcher.end()
        #     else:
        #         raise ParseException("bad token at line " + line_no)
        for match_tuple in self.pattern.findall(line):
            if match_tuple[0]:
                self.add_token(line_no, match_tuple)
        # else:
        #     raise ParseException("bad token at line " + str(line_no))

        self.queue.append(IdToken(line_no, mytoken.Token.EOL))

    def add_token(self, line_no, match_tuple):
        if match_tuple:
            if match_tuple[1] == '':
                if match_tuple[2]:
                    token = NumToken(line_no, int(match_tuple[2]))
                elif match_tuple[3]:
                    token = StrToken(line_no, self.to_string_literal(match_tuple[3]))
                else:
                    token = IdToken(line_no, match_tuple[0])
                self.queue.append(token)

    def to_string_literal(self, s):
        sb = []
        len = len(s) - 1
        skip = False
        for i, c in enumerate(s):
            if skip:
                skip = False
                continue
            if c == '\\' and i + 1 < len:
                c2 = s[i + 1]
                if c2 == '"' or c2 == '\\':
                    c = c2
                    skip = True
                elif c2 == 'n':
                    c = '\n'
                    skip = True
            sb.append(c)
        return ''.join(sb)


class NumToken(mytoken.Token):
    def __init__(self, line, v):
        super(NumToken, self).__init__(line)
        self.value = v

    def is_number(self):
        return True

    def get_text(self):
        return str(self.value)

    def get_number(self):
        return self.value

class IdToken(mytoken.Token):
    def __init__(self, line, _id):
        super(IdToken, self).__init__(line)
        self.text = _id

    def is_identifier(self):
        return True

    def get_text(self):
        return str(self.text)

class StrToken(mytoken.Token):
    def __init__(self, line, s):
        super(StrToken, self).__init__(line)
        self.literal = s

    def is_string(self):
        return True

    def get_text(self):
        return str(self.literal)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
