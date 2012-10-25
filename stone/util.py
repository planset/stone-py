# -*- coding: utf-8 -*-

import inspect
import types

class HashSet(object):
    """A set abstraction supporting the basic set operations.

    This implementation requires that all elements are hashable,
    which implies that elements must not mutate while contained.
    """
    def __init__(self, elements = []):
        """Initializes a new HashSet."""
        self.__elements = {}
        for e in elements:
            self.__elements[e] = 1
            
    def __contains__(self, element):
        """Returns true iff this set contains element."""
        return self.__elements.has_key(element)

    def __eq__(self, set):
        """Returns true iff x == y for all elements in self, set."""
        if not isinstance(set, HashSet):
            return 0
        for x in self.list():
            if not (x in set): return 0
        for x in set.list():
            if not (x in self): return 0
        return 1

    def __len__(self):
        """Returns the number of elements in this set."""
        return len(self.__elements)

    def __ne__(self, set):
        """Returns true iff this set is not equal to set.""" 
        return not self.__eq__(set)

    def __repr__(self):
        """Returns a debugging string representation of this set."""
        return "HashSet(" + repr(self.list()) + ")"

    def __str__(self):
        """Returns a string representation of this set."""
        return "{" + ",".join(map(str, self.list())) + "}" 

    # Element access:

    def append(self, element):
        """Adds element to this set."""
        self.__elements[element] = 1

    def contains(self, element):
        """Returns true iff this set contains element."""
        return self.__contains__(element)

    def remove(self, element):
        """Removes element from this set."""
        try:
            del self.__elements[element]
        except KeyError:
            pass

    def list(self):
        """Returns the elements of this set in a list."""
        return self.__elements.keys()

    # Information:

    def empty(self):
        """Returns true iff this set is empty."""
        return len(self.__elements) == 0

    # Set operations:

    def union(self, s):
        """Returns the union of this set and s."""
        return HashSet(self.list() + s.list())

    def intersection(self, s):
        """Returns the intersection of this set and s."""
        return HashSet(filter(lambda e,s=s: e in s, self.list()))

    def difference(self, s):
        """Returns the difference of this set and s."""
        return HashSet(filter(lambda e,s=s: e not in s, self.list()))

    def cartesian(self,s):
        """Returns the Cartesian product of this set and s."""
        p = []
        for i in self.list():
            for j in s.list():
                p.append((i,j))
        return HashSet(p)
    


def reviser(original_class):
    '''Add methods defined in the derived class to the base class.
    '''
    parent_class = original_class.__bases__[0]
    parent_class_init = parent_class.__init__
    def _init(self, *args, **kwargs):
        parent_class_init(self, *args, **kwargs)
        for k,v in original_class.__dict__.iteritems():
            if not inspect.isfunction(v):
                continue
            self.__dict__[k] = types.MethodType(v, self)
    parent_class.__init__ = _init




# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4