# -*- coding: utf-8 -*-

class LineNumberReader(object):
    def __init__(self, f):
        if isinstance(f, type(file)):
            raise TypeError('f is reuqired file.\n{}'.format(f.__type__))
        self.f = f
        self.cur_line = 0

    def readline(self):
        self.cur_line += 1
        return self.f.readline()

    def get_line_number(self):
        return self.cur_line


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
