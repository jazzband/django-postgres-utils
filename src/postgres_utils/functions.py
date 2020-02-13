"""
Database Functions
==================

Django provides a way for users to use functions provided by the underlying database as annotations,
aggregations, or filters. Functions are also expressions, so they can be used and combined with
other expressions like aggregate functions.

However the list of `PostgreSQL specific functions in Django <functions>`_ is very limited.

.. _functions: https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/functions/
"""
from django.db.models import Subquery, Func, Value


class ArraySubquery(Subquery):
    """
    Convert sub-query results to array

    While Django's original :py:class:`django.db.models.Subquery` is allowed to return only one
    match, this subquery is converted into an array and can return all matches, e.g.:

    .. code-block:: python

        sub_q = Topping.objects.filter(pizza=OuterRef("id"), vegan=True).values("name")
        qs = Pizza.objects.annotate(vegan_toppings=ArraySubquery(sub_q))

    :param queryset: The queryset to be executed as subquery.
    """
    template = 'ARRAY(%(subquery)s)'


class RegexpReplace(Func):
    """
    Use regular expression to replace value in field

    .. note:: This might become available in Django in the future:
              https://code.djangoproject.com/ticket/28805

    .. code-block:: python

        Topping.objects \\
            .filter(name__contains="Onion") \\
            .annotate(onion_color=RegexpReplace("name", " *Onion$", ""))

    :param expression: The expression/field to work on
    :param pattern: The regular expression pattern to match
    :param replacement: The replacement string for matches
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

    .. code-block:: python

        Topping.objects \\
            .filter(name__contains="Sauce") \\
            .annotate(souce_type=Substring("name", "[A-Za-z]+(?= Sauce)")) \\
            .values("name", "souce_type") \\
            .order_by("name")

    :param expression: The expression/field to work on
    :param pattern: The regular expression pattern to match
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
