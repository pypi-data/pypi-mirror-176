from .pipeable import pipeable
import operator

is_lt = pipeable(lambda b, a: operator.lt(a, b))
is_le = pipeable(lambda b, a: operator.le(a, b))
is_eq = pipeable(lambda b, a: operator.eq(a, b))
is_ne = pipeable(lambda b, a: operator.ne(a, b))
is_ge = pipeable(lambda b, a: operator.ge(a, b))
is_gt = pipeable(lambda b, a: operator.gt(a, b))


not_ = pipeable(lambda obj: operator.not_(obj))
truth = pipeable(lambda obj: operator.truth(obj))
is_ = pipeable(lambda a, b): operator.is_(a, b))
is_not = pipeable(lambda a, b): operator.is_not(a, b))
