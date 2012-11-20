# -*- coding: utf-8 -*-

import inspect
import functools

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
    


original_super = super
def _super(cls, obj):
    if obj.__dict__.has_key('original_obj'):
        original_obj = obj.original_obj
    else:
        original_obj = obj

    if original_obj.__class__.__dict__.has_key('__reviser__'):
        if cls in original_obj.__reviser__:
            parent_class = _get_parent_class(cls)

            class _cls(parent_class):
                def __init__(self, obj):
                    self.original_obj = original_obj if obj.__dict__.has_key('original_obj') else obj
                    self._is_calling = False

                def __getattribute__(self, attrname):
                    if attrname == 'original_obj':
                        return object.__getattribute__(self, attrname)
                    m = object.__getattribute__(self, attrname)
                    if inspect.ismethod(m):
                        # 元のメソッドを呼び出したあと、オブジェクトの属性を更新する。
                        def _m(self, *args, **kwargs):
                            if not self._is_calling:
                                self._is_calling = True
                                for k,v in inspect.getmembers(self.original_obj):
                                    if k.startswith('__') or inspect.ismethod(v) or isinstance(v, functools.partial):
                                        continue
                                    self.__dict__[k] = v
                                result = m(*args, **kwargs)
                                self._is_calling = False
                                for k,v in inspect.getmembers(self):
                                    if k.startswith('__') or inspect.ismethod(v):
                                        continue
                                    self.original_obj.__dict__[k] = v
                                self._is_calling = False
                                return result 
                            else:
                                return m(*args, **kwargs)

                        return functools.partial(_m, self)
                    return m
            return _cls(obj)

    return original_super(cls, obj)

super = _super

def _get_super_classes(cls):
    mro = inspect.getmro(cls)
    return mro[1:-1]

def _get_parent_class(cls):
    return _get_super_classes(cls)[0]

def _get_base_class(cls):
    '''@reviserしているクラスであれば更に基底クラス方向に検索する。
    @reviserしていないクラスがあれば、そのクラスを返す。
    '''
    classes = inspect.getmro(cls)[1:-1]
    if len(classes) == 0:
        return cls
    c = classes[0]
    if c.__dict__.has_key('is_reviser'):
        return _get_base_class(c)
    else:
        return c


def _search_reviser(obj, attrname):
    if obj.__class__ != type or obj.__dict__.has_key('__reviser__'):
        for cls in obj.__reviser__:
            if cls.__dict__.has_key(attrname):
                v = cls.__dict__[attrname]
                if inspect.isfunction(v):
                    return v
    return None

def _search_members(cls, attrname):
    if attrname != '__base_class_init__':
        members = dict(inspect.getmembers(cls))
        if members.has_key(attrname):
            v = members[attrname]
            if inspect.isfunction(v):
                return v
    return None

def _lookup_attrname(cls, attrname, compset):
    for parent_cls in cls.__bases__:
        if parent_cls in compset:
            continue 
        compset.add(parent_cls)

        v = _search_reviser(parent_cls, attrname)
        v = v or _search_members(parent_cls, attrname)
        v = v or _lookup_attrname(parent_cls, attrname, compset) 

        if v:
            return v

    return None

def _getattribute(self, attrname, *args, **kwargs):
    '''__init__は__getattribute__は呼ばれない'''

    #特殊メソッドは今のところ先に返しちゃう
    if attrname.startswith('__') and attrname.endswith('__'):
        return object.__getattribute__(self, attrname)

    if attrname != '__reviser__':
        v = _search_reviser(self, attrname)
        v = v or _search_members(self.__class__, attrname)
        v = v or _lookup_attrname(self.__class__, attrname, set())
        if v:
            return functools.partial(v, self)

    return object.__getattribute__(self, attrname)


def reviser(original_class):
    base_class = _get_base_class(original_class)
    if not base_class.__dict__.has_key('__reviser__'):
        base_class.__reviser__ = []
    base_class.__reviser__.insert(0, original_class)
    base_class.__getattribute__ = _getattribute
    
    __base_class_init__ = base_class.__init__
    def _init(self, *args, **kwargs):
        return __base_class_init__(self, *args, **kwargs)
    base_class.__init__ = _init
    
    original_class.is_reviser = True

    return original_class


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
