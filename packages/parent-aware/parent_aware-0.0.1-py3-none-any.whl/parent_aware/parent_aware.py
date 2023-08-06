'''
parent_aware is a decorator for dataclasses. When used on nested dataclasses, it gives access
to the 'parent' element of the dataclasss. The parent is the dataclass that the child is placed on.
'''
import functools
import logging
import typing

logger = logging.getLogger('parent_aware_dataclass')

class _ParentAware:
    ''' Use this class / inheritance to mark this class as wanting references to parents '''
    pass

def _walk_obj(obj: typing.Any,
             func: typing.Callable,
             visited: typing.Optional[list]=None,
             additional_depth: typing.Union[int, float]=float('inf')):
    '''
    Walks regular attributes on the given object. On each attribute, runs the given function.
    Internally keeps track of visited objects to avoid infinite recursion.
    Additional_depth is used to say how deep we should go. (Each layer subtracts 1)
    '''
    visited = visited or []

    logger.debug(f"_walk_obj sees: {repr(obj)} additional_depth: {additional_depth}")

    if obj not in visited and additional_depth:
        visited.append(obj)

        if hasattr(obj, '__dict__'):
            for key, value in list(obj.__dict__.items()):
                _walk_obj(value, func, visited, additional_depth - 1)
                obj.__dict__[key] = func(value)
        elif isinstance(obj, dict):
            for key, value in list(obj.items()):
                _walk_obj(value, func, visited, additional_depth - 1)
                obj[key] = func(value)
        elif isinstance(obj, list):
            for idx, itm in enumerate(obj):
                _walk_obj(itm, func, visited, additional_depth - 1)
                obj[idx] = func(itm)


def parent_aware(klass: typing.Optional[typing.Type]=None,
                 parents_name: str='parents'):
    '''
    Used as a class decorator. Marks an object as having its immediate children
    being aware of their parent.

    @parent_aware
    or
    @parent_aware(parents_name='name_to_use_instead_of_parents')
    or
    @parent_aware()

    Useful for dataclasses.
    '''
    def high_level_wrapper(_klass):
        @functools.wraps(_klass)
        def wrapper(*args, **kwargs):
            KLASS = type(_klass.__name__, (_klass, _ParentAware), {})
            ret = KLASS(*args, **kwargs)
            def walker(obj):
                if isinstance(obj, _ParentAware):
                    parents = getattr(obj, parents_name, [])
                    if ret not in parents:
                        parents.append(ret)
                        setattr(obj, parents_name, parents)

                return obj

            _walk_obj(ret, walker)
            return ret

        return wrapper

    if klass is None:
        return high_level_wrapper
    else:
        return high_level_wrapper(klass)
