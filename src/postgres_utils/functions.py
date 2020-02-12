from django.db.models import Subquery, Func, Value


class ArraySubquery(Subquery):
    """
    Convert sub-query results to array
    """
    template = 'ARRAY(%(subquery)s)'


class RegexpReplace(Func):
    """
    Use regular expression to replace value in field

    .. note:: This might become available in Django in the future:
              https://code.djangoproject.com/ticket/28805
    """
    function = 'REGEXP_REPLACE'

    def __init__(self, expression, pattern, replacement, **extra):
        if not hasattr(pattern, 'resolve_expression'):
            if not isinstance(pattern, str):
                raise TypeError("'pattern' must be a string")
            pattern = Value(pattern)
        if not hasattr(replacement, 'resolve_expression'):
            if not isinstance(replacement, str):
                raise TypeError("'replacement' must be a string")
            replacement = Value(replacement)
        expressions = [expression, pattern, replacement]
        super().__init__(*expressions, **extra)


class Substring(Func):
    """
    Use regular expression to extract a substring from field
    """
    arg_joiner = ' FROM '
    function = 'SUBSTRING'

    def __init__(self, expression, pattern):
        if not hasattr(pattern, 'resolve_expression'):
            if not isinstance(pattern, str):
                raise TypeError("'pattern' must be a string")
            pattern = Value(pattern)
        super().__init__(expression, pattern)

    def __repr__(self):
        args = self.arg_joiner.join(str(arg) for arg in self.source_expressions)
        return "{}({})".format(self.__class__.__name__, args)
