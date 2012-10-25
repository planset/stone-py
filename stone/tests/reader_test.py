from stone import reader
import unittest

class TestLineNumberReader(unittest.TestCase):
    def test_init_not_file(self):
        self.assertRaises(TypeError, reader.LineNumberReader(1))

    def test_init(self):
        import tempfile
        f = tempfile.TemporaryFile()
        f.write(b'hoge\nhoge\nhoge')
        f.seek(0)
        r = reader.LineNumberReader(f)
        self.assertIsNotNone(r)

    def test_read_get_line_number(self):
        import tempfile
        f = tempfile.TemporaryFile()
        f.write('hoge\nhoge\nhoge')
        f.seek(0)
        r = reader.LineNumberReader(f)
        self.assertEqual('hoge\n', r.readline())
        self.assertEqual(1, r.get_line_number())

if __name__ == '__main__':
    unittest.main()
