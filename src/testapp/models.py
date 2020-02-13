from django.db import models


class NaturalKeyManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class BaseNameModel(models.Model):
    name = models.CharField(max_length=32, unique=True, null=False, blank=False)
    objects = NaturalKeyManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

    class Meta:
        abstract = True


class Topping(BaseNameModel):

    veggy = models.BooleanField()
    vegan = models.BooleanField()


class Pizza(BaseNameModel):
    toppings = models.ManyToManyField(Topping)
