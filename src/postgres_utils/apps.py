from inspect import isclass

from django.apps import AppConfig
from django.db.models import fields, Lookup

from . import lookups


class PostgresUtilsConfig(AppConfig):
    name = 'postgres_utils'

    def ready(self):
        super().ready()

        for lookup in dir(lookups):
            lookup = getattr(lookups, lookup, None)
            if isclass(lookup) and issubclass(lookup, Lookup):
                fields.CharField.register_lookup(lookup)
