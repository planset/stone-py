from stone import basic_parser, lexer, mytoken

import tempfile
f = tempfile.TemporaryFile()
f.write("""
even = 0
odd = 0
i = 1
while i < 10 {
    if i % 2 == 0 {
        even = even + i
    } else {
        odd = odd + i
    }
    i = i + 1
}
even + odd
""")
f.seek(0)

l = lexer.Lexer(f)
bp = basic_parser.BasicParser()
while l.peek(0) != mytoken.Token.EOF:
    ast = bp.parse(l)
    print '=>', ast.to_string()

f.close()

