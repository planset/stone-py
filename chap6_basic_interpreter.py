# -*- coding: utf-8 -*-

from stone import basic_parser, lexer, mytoken
from stone.myast import statement as stmt
from chap6 import basic_env

from chap6 import basic_evaluator


class BasicInterpreter(object):
    def testcode(self):
        return """
sum = 0
i = 1
while i < 10 {
    sum = sum + i
    i = i + 1
}
sum
if sum == 45 {
    hoge = 10
}"""

    def _make_temporary_file(self):
        import tempfile

        f = tempfile.TemporaryFile()
        f.write(self.testcode())
        f.seek(0)
        return f

    def main(self):
        self.run(basic_parser.BasicParser(),
                 basic_env.BasicEnv())

    def run(self, bp, env):
        f = self._make_temporary_file()
        try:
            l = lexer.Lexer(f)
            while l.peek(0) != mytoken.Token.EOF:
                t = bp.parse(l)
                if not isinstance(t, stmt.NullStmnt):
                    r = t.eval(env)
                    print '=>' + str(r)
        finally:
            f.close()
            
    def run_parser(self, bp, env):
        f = self._make_temporary_file()
        try:
            l = lexer.Lexer(f)
            while l.peek(0) != mytoken.Token.EOF:
                t = bp.parse(l)
                print t.to_string()
        finally:
            f.close()

if __name__ == '__main__':
    BasicInterpreter().main()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
