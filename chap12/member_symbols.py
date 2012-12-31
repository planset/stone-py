
from chap11 import symbols

class MemberSymbols(symbols.Symbols):
    METHOD = -1
    FIELD = -2
    
    def __init__(self, outer, _type):
        super(MemberSymbols, self).__init__(outer)
        self._type = _type

    def get(self, key, nest):
        index = self.table.get(key)
        if index is None:
            if self.outer is None:
                return None
            else:
                return self.outer.get(key, nest)
        else:
            return self.Location(self._type, int(index))

    def put(self, key):
        loc = self.get(key, 0)
        if loc is None:
            return self.Location(self._type, self.add(key))
        else:
            return loc



