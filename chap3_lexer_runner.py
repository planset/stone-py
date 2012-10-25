from __future__ import print_function
from stone import lexer, mytoken

import tempfile
f = tempfile.TemporaryFile()
f.write("""if (i==1) {
 a=1
 }
while i < 10 {
    sum = sum + i
    i = i + 1
}
sum
""")
f.seek(0)

l = lexer.Lexer(f)
while True:
    t = l.read()
    if t is mytoken.Token.EOF:
        print('break')
        break
    print("=> " + t.get_text())


