
from stone import exception
from chap11 import symbols

class SymbolThis(symbols.Symbols):
    NAME = 'this'

    def __init__(self, outer):
        super(SymbolThis, self).__init__(outer)
        self.add(self.NAME)

    def put_new(self, key):
        raise exception.StoneException('fatal')

    def put(self, key):
        loc = self.outer.put(key)
        if loc.nest >= 0:
            loc.nest += 1
        return loc

