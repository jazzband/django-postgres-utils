from django.db.models import Count, OuterRef
from django.test import TestCase

from postgres_utils.functions import ArraySubquery, RegexpReplace, Substring
from testapp.models import Pizza, Topping


# Create your tests here.
class LookUpTest(TestCase):
    fixtures = ["recipes.yaml", ]

    def test_notregex(self):
        with self.subTest("Primary model"):
            qs = Pizza.objects.filter(name__noregex="[ ]+")
            self.assertEqual(qs.count(), 3)
            self.assertEqual(
                set(qs.values_list("name", flat=True)),
                {"Margherita", "Salami", "Funghi"}
            )

        with self.subTest("Sub-model"):
            qs = Pizza.objects.exclude(toppings__name__regex="Sauce|Onion").distinct()
            self.assertFalse(qs.exists())

            # Notice the difference:
            # Now we are only excluding toppings, not entire pizzas 😉
            qs = Pizza.objects \
                .filter(toppings__name__noregex="Sauce|Onion", name__in=["Funghi", "Salami"])\
                .values("name")\
                .annotate(num_toppings=Count("toppings"))\
                .values("name", "num_toppings")\
                .order_by()

            self.assertEqual(
                sorted(qs, key=lambda x: x.get("name")),
                [{'name': 'Funghi', 'num_toppings': 3}, {'name': 'Salami', 'num_toppings': 2}]
            )

    def test_inotregex(self):
        qs = Pizza.objects \
            .filter(toppings__name__inoregex="sauce|onion", name__in=["Funghi", "Teriyaki Chicken"])\
            .values("name")\
            .annotate(num_toppings=Count("toppings"))\
            .values("name", "num_toppings")\
            .order_by()

        self.assertEqual(
            sorted(qs, key=lambda x: x.get("name")),
            [{'name': 'Funghi', 'num_toppings': 3}, {'name': 'Teriyaki Chicken', 'num_toppings': 3}]
        )

    def test_notin(self):
        with self.subTest("Primary model"):
            qs = Pizza.objects.exclude(name__in=["Salami", "Margherita"])
            self.assertEqual(qs.count(), 3)

            qs = Pizza.objects.filter(name__notin=["Salami", "Margherita"])
            self.assertEqual(qs.count(), 3)

        with self.subTest("Sub-model"):
            # Original `__in` lokkup excludes all pizzas with at least one matching topping
            qs = Pizza.objects.exclude(toppings__name__in=["Sesame", "Salami"])
            self.assertEqual(qs.count(), 3)
            self.assertEqual(qs.distinct().count(), 3)

            # `__notin` just filters out matching toppings
            qs = Pizza.objects.filter(toppings__name__notin=["Sesame", "Salami"])
            self.assertEqual(qs.count(), 19)
            self.assertEqual(qs.distinct().count(), 5)


class FunctionTest(TestCase):
    fixtures = ["recipes.yaml", ]

    def test_array_subquery(self):
        sub_q = Topping.objects.filter(pizza=OuterRef("id"), vegan=True).values("name")
        qs = Pizza.objects\
            .annotate(vegan_toppings=ArraySubquery(sub_q))\
            .values("name", "vegan_toppings")

        self.assertTrue(all(isinstance(pizza.get("vegan_toppings", None), list) for pizza in qs))

        pizza_salami = [pizza for pizza in qs if pizza["name"] == "Salami"][0]
        self.assertEqual(pizza_salami["vegan_toppings"], ['Tomato Sauce'])

    def test_regex_replace(self):
        qs = Topping.objects\
            .filter(name__contains="Onion")\
            .annotate(onion_color=RegexpReplace("name", " *Onion$", ""))\
            .values("name", "onion_color")\
            .order_by("name")

        self.assertEqual(
            list(qs),
            [{"name": "Green Onion", "onion_color": "Green"}, {"name": "Onion", "onion_color": ""},
             {"name": "Red Onion", "onion_color": "Red"}]
        )

    def test_substring(self):
        qs = Topping.objects\
            .filter(name__contains="Sauce")\
            .annotate(souce_type=Substring("name", "[A-Za-z]+(?= Sauce)"))\
            .values("name", "souce_type")\
            .order_by("name")

        self.assertEqual(
            list(qs),
            [{'name': 'BBQ Sauce', 'souce_type': 'BBQ'},
             {'name': 'Teriyaki Sauce', 'souce_type': 'Teriyaki'},
             {'name': 'Tomato Sauce', 'souce_type': 'Tomato'}, ]
        )
