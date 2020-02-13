"""
LookUps
=======

Django offers a series of built-in lookups that can be used in queries, but
sometimes one needs additional lookups to take full advantage of an underlying
database. Therefore Django allows developers to define
`custom lookups <https://docs.djangoproject.com/en/2.2/howto/custom-lookups/>`_.

This app provides the following lookups:
"""
# pylint: disable=line-too-long
from django.db.models import Lookup
from django.db.models.lookups import In


class NotRegex(Lookup):
    """
    ``__noregex`` matches rows that do not match a RegExp

    Use as follows:

    .. code-block:: python

        qs = Model.objects.filter(charfield__noregex="pattern")

    See also `PostgreSQL: POSIX Regular Expressions <https://www.postgresql.org/docs/10/functions-matching.html#FUNCTIONS-POSIX-REGEXP>`_
    """
    lookup_name = "noregex"
    _operator = "!~"
    prepare_rhs = False

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s %s %s' % (lhs, self._operator, rhs), params


class INotRegex(Lookup):
    """
    ``__inoregex`` matches rows that do not match a case-insensitive RegExp
    """
    lookup_name = "inoregex"
    _operator = "!~*"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s %s %s' % (lhs, self._operator, rhs), params


class NotIn(In):
    """
    ``__notin`` matches rows with values not in the list

    Use as follows:

    .. code-block:: python

        qs = Model.objects.filter(somefield__notin=[value1, value2, ...])
    """
    lookup_name = "notin"

    def get_rhs_op(self, connection, rhs):
        return 'NOT IN %s' % rhs
