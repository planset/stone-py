import tempfile
import unittest

from stone import lexer, mytoken


class TestLexer(unittest.TestCase):
    def test_init(self):
        f = tempfile.TemporaryFile()
        f.write("""while i < 10 {
            sum = sum + i
            i = i + 1
            }
            sum""")
        f.seek(0)
        l = lexer.Lexer(f)
        self.assertIsNotNone(l)
        f.close()

    def test_read(self):
        f = tempfile.TemporaryFile()
        f.write("""while i < 10 {
            sum = sum + i
            i = i + 1
            }
            sum""")
        f.seek(0)
        l = lexer.Lexer(f)
        self.assertEqual('while', l.read().get_text())
        self.assertEqual('i', l.read().get_text())
        self.assertEqual('<', l.read().get_text())
        self.assertEqual('10', l.read().get_text())
        self.assertEqual('{', l.read().get_text())
        self.assertEqual(mytoken.Token.EOL, l.read().get_text())
        self.assertEqual('sum', l.read().get_text())
        self.assertEqual('=', l.read().get_text())
        self.assertEqual('sum', l.read().get_text())
        self.assertEqual('+', l.read().get_text())
        self.assertEqual('i', l.read().get_text())
        self.assertEqual(mytoken.Token.EOL, l.read().get_text())
        self.assertEqual('i', l.read().get_text())
        self.assertEqual('=', l.read().get_text())
        self.assertEqual('i', l.read().get_text())
        self.assertEqual('+', l.read().get_text())
        self.assertEqual('1', l.read().get_text())
        self.assertEqual(mytoken.Token.EOL, l.read().get_text())
        self.assertEqual('}', l.read().get_text())
        self.assertEqual(mytoken.Token.EOL, l.read().get_text())
        self.assertEqual('sum', l.read().get_text())
        self.assertEqual(mytoken.Token.EOL, l.read().get_text())


if __name__ == '__main__':
    unittest.main()

