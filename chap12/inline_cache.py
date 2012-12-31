
from stone.util import reviser, super
from stone import exception
from . import obj_optimizer, opt_stone_object


@reviser
class DotEx2(obj_optimizer.DotEx):
    def __init__(self, list_of_astree):
        super(DotEx2, self).__init__(list_of_astree)
        self.class_info = None
        self.is_field = False
        self.index = 0

    def eval(self, env, value):
        if isinstance(value, opt_stone_object.OptStoneObject):
            target = value
            if target.class_info() != self.class_info:
                self.update_cache(target)
            if self.is_field:
                return target.read(self.index)
            else:
                return target.method(self.index)
        else:
            return super(DotEx2, self).eval(env, value)

    def update_cache(self, target):
        member = self.name()
        self.class_info = target.class_info()
        i = self.class_info.field_index(member)
        if i is not None:
            self.is_field = True
            self.index = i
            return
        i = self.class_info.method_index(member)
        if i is not None:
            self.is_field = False
            self.index = i
            return
        raise exception.StonException('bad member access: ' + member, self)

class AssignEx2(obj_optimizer.AssignEx):
    def __init__(self, list_of_astree):
        super(AssignEx2, self).__init__(self, list_of_astree)
        self.class_info = None
        self.index = 0

    def set_field(self, obj, expr, rvalue):
        if obj.class_info != self.class_info:
            member = expr.name()
            self.class_info = obj.class_info
            i = self.class_info.field_index(member)
            if i is None:
                raise exception.StoneException('bad member access: ' + member, self)
            self.index = i
        obj.write(self.index, rvalue)
        return rvalue





