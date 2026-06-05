from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Cook, DishType, Dish, Ingredient
from .forms import (
    CookCreationForm,
    CookExperienceUpdateForm,
    CooksUsernameSearchForm,
    DishTypeForm,
    DishTypesNameSearchForm,
    DishForm,
    DishesNameSearchForm,
    IngredientForm,
    IngredientsNameSearchForm,
)


class CookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Cook.objects.create_user(
            username="chef1",
            first_name="Gordon",
            last_name="Ramsay",
            years_of_experience=20,
            email="gordon@restaurant.com",
            password="secret123"
        )

    def test_string_representation(self):
        cook = Cook.objects.get(username="chef1")
        expected = f"{cook.first_name} {cook.last_name} ({cook.username})"
        self.assertEqual(str(cook), expected)

    def test_years_of_experience_default(self):
        cook = Cook.objects.create_user(
            username="newchef",
            password="secret123"
        )
        self.assertEqual(cook.years_of_experience, 0)

    def test_get_absolute_url(self):
        cook = Cook.objects.get(username="chef1")
        expected_url = reverse("kitchen:cook-detail", kwargs={"pk": cook.pk})
        self.assertEqual(cook.get_absolute_url(), expected_url)


class DishTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        DishType.objects.create(name="Appetizer")
        DishType.objects.create(name="Main Course")

    def test_string_representation(self):
        dish_type = DishType.objects.get(name="Appetizer")
        self.assertEqual(str(dish_type), "Appetizer")

    def test_ordering(self):
        dish_types = DishType.objects.all()
        self.assertEqual(
            list(dish_types),
            list(dish_types.order_by("name"))
        )


class DishModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dish_type = DishType.objects.create(name="Dessert")
        cls.cook = Cook.objects.create_user(
            username="pastrychef",
            first_name="Pierre",
            last_name="Hermé",
            years_of_experience=15,
            password="secret123"
        )
        cls.ingredient = Ingredient.objects.create(name="Chocolate")
        cls.dish = Dish.objects.create(
            name="Chocolate Cake",
            description="Rich chocolate cake",
            price="25.00",
            dish_type=cls.dish_type
        )
        cls.dish.cooks.add(cls.cook)
        cls.dish.ingredients.add(cls.ingredient)

    def test_string_representation(self):
        self.assertEqual(str(self.dish), "Chocolate Cake")

    def test_dish_type_relationship(self):
        self.assertEqual(self.dish.dish_type.name, "Dessert")

    def test_cooks_relationship(self):
        self.assertEqual(self.dish.cooks.count(), 1)
        self.assertEqual(self.dish.cooks.first().username, "pastrychef")

    def test_ingredients_relationship(self):
        self.assertEqual(self.dish.ingredients.count(), 1)
        self.assertEqual(self.dish.ingredients.first().name, "Chocolate")

    def test_get_absolute_url(self):
        expected_url = reverse(
            "kitchen:dish-detail",
            kwargs={"pk": self.dish.pk}
        )
        self.assertEqual(self.dish.get_absolute_url(), expected_url)


class IngredientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Ingredient.objects.create(name="Tomato")
        Ingredient.objects.create(name="Basil")

    def test_string_representation(self):
        ingredient = Ingredient.objects.get(name="Tomato")
        self.assertEqual(str(ingredient), "Tomato")


class FormTests(TestCase):
    def test_dish_type_form_valid(self):
        form = DishTypeForm(data={"name": "Soup"})
        self.assertTrue(form.is_valid())

    def test_dish_type_form_blank(self):
        form = DishTypeForm(data={"name": ""})
        self.assertFalse(form.is_valid())

    def test_ingredient_form_valid(self):
        form = IngredientForm(data={"name": "Garlic"})
        self.assertTrue(form.is_valid())

    def test_cooks_username_search_form_valid(self):
        form = CooksUsernameSearchForm(data={"username": "chef"})
        self.assertTrue(form.is_valid())

    def test_cooks_username_search_form_blank(self):
        form = CooksUsernameSearchForm(data={"username": ""})
        self.assertTrue(form.is_valid())

    def test_dish_types_name_search_form_valid(self):
        form = DishTypesNameSearchForm(data={"name": "app"})
        self.assertTrue(form.is_valid())

    def test_dish_types_name_search_form_blank(self):
        form = DishTypesNameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_dishes_name_search_form_valid(self):
        form = DishesNameSearchForm(data={"name": "cake"})
        self.assertTrue(form.is_valid())

    def test_dishes_name_search_form_blank(self):
        form = DishesNameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_ingredients_name_search_form_valid(self):
        form = IngredientsNameSearchForm(data={"name": "tom"})
        self.assertTrue(form.is_valid())

    def test_ingredients_name_search_form_blank(self):
        form = IngredientsNameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_cook_creation_form_valid(self):
        form = CookCreationForm(data={
            "username": "newchef",
            "first_name": "New",
            "last_name": "Chef",
            "years_of_experience": 5,
            "email": "newchef@restaurant.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
        })
        self.assertTrue(form.is_valid())

    def test_cook_experience_update_form_valid(self):
        cook = Cook.objects.create_user(
            username="experienceup",
            password="secret123"
        )
        form = CookExperienceUpdateForm(
            instance=cook,
            data={"years_of_experience": 10},
        )
        self.assertTrue(form.is_valid())

    def test_dish_form_valid(self):
        dish_type = DishType.objects.create(name="Test Type")
        cook = Cook.objects.create_user(
            username="formcook",
            password="secret123"
        )
        ingredient = Ingredient.objects.create(name="Test Ingredient")
        form = DishForm(data={
            "name": "Test Dish",
            "description": "Test description",
            "price": "15.00",
            "dish_type": dish_type.id,
            "cooks": [cook.id],
            "ingredients": [ingredient.id],
        })
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dish_type1 = DishType.objects.create(name="Appetizer")
        cls.dish_type2 = DishType.objects.create(name="Main Course")
        cls.cook1 = Cook.objects.create_user(
            username="chef1",
            first_name="Anna",
            last_name="Smith",
            years_of_experience=10,
            password="secret"
        )
        cls.cook2 = Cook.objects.create_user(
            username="chef2",
            first_name="Bob",
            last_name="Jones",
            years_of_experience=5,
            password="secret"
        )
        cls.ingredient1 = Ingredient.objects.create(name="Tomato")
        cls.ingredient2 = Ingredient.objects.create(name="Basil")
        cls.dish1 = Dish.objects.create(
            name="Bruschetta",
            description="Grilled bread with tomato",
            price="12.00",
            dish_type=cls.dish_type1
        )
        cls.dish1.cooks.add(cls.cook1)
        cls.dish1.ingredients.add(cls.ingredient1, cls.ingredient2)
        cls.dish2 = Dish.objects.create(
            name="Pasta Carbonara",
            description="Classic pasta",
            price="18.00",
            dish_type=cls.dish_type2
        )
        cls.dish2.cooks.add(cls.cook2)
        cls.dish3 = Dish.objects.create(
            name="Caesar Salad",
            description="Fresh salad",
            price="14.00",
            dish_type=cls.dish_type1
        )
        cls.dish3.cooks.add(cls.cook1, cls.cook2)

    def setUp(self):
        self.client.login(username=self.cook1.username, password="secret")

    def test_index_view(self):
        response = self.client.get(reverse("kitchen:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cooks")
        self.assertContains(response, "Dishes")
        self.assertContains(response, "Dish Types")

    def test_cook_list_view(self):
        response = self.client.get(reverse("kitchen:cook-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cook1.username)
        self.assertContains(response, self.cook2.username)
        self.assertEqual(len(response.context["cook_list"]), 2)

    def test_cook_list_search(self):
        response = self.client.get(
            reverse("kitchen:cook-list") + "?username=chef1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<strong>chef1</strong>")

        response = self.client.get(
            reverse("kitchen:cook-list") + "?username=chef2"
        )
        self.assertContains(response, "<strong>chef2</strong>")

    def test_dish_type_list_view(self):
        response = self.client.get(reverse("kitchen:dish-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dish_type1.name)
        self.assertContains(response, self.dish_type2.name)
        self.assertEqual(len(response.context["dish_type_list"]), 2)

    def test_dish_type_list_search(self):
        response = self.client.get(
            reverse("kitchen:dish-type-list") + "?name=app"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dish_type1.name)
        self.assertNotContains(response, self.dish_type2.name)

        response = self.client.get(
            reverse("kitchen:dish-type-list") + "?name=main"
        )
        self.assertContains(response, self.dish_type2.name)
        self.assertNotContains(response, self.dish_type1.name)

    def test_dish_list_view(self):
        response = self.client.get(reverse("kitchen:dish-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dish1.name)
        self.assertContains(response, self.dish2.name)
        self.assertContains(response, self.dish3.name)
        self.assertEqual(len(response.context["dish_list"]), 3)

    def test_dish_list_search(self):
        response = self.client.get(
            reverse("kitchen:dish-list") + "?name=bruschetta"
        )
        self.assertContains(response, self.dish1.name)
        self.assertNotContains(response, self.dish2.name)
        self.assertNotContains(response, self.dish3.name)

        response = self.client.get(
            reverse("kitchen:dish-list") + "?name=pasta"
        )
        self.assertContains(response, self.dish2.name)
        self.assertNotContains(response, self.dish1.name)
        self.assertNotContains(response, self.dish3.name)

    def test_ingredient_list_view(self):
        response = self.client.get(reverse("kitchen:ingredient-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ingredient1.name)
        self.assertContains(response, self.ingredient2.name)
        self.assertEqual(len(response.context["ingredient_list"]), 2)

    def test_ingredient_list_search(self):
        response = self.client.get(
            reverse("kitchen:ingredient-list") + "?name=tom"
        )
        self.assertContains(response, self.ingredient1.name)
        self.assertNotContains(response, self.ingredient2.name)

    def test_toggle_assign_to_dish_view(self):
        self.assertNotIn(self.dish2, self.cook1.dishes_prepared.all())
        response = self.client.get(
            reverse("kitchen:toggle-dish-assign", args=[self.dish2.id])
        )
        self.assertRedirects(
            response,
            reverse("kitchen:dish-detail", args=[self.dish2.id])
        )
        self.cook1.refresh_from_db()
        self.assertIn(self.dish2, self.cook1.dishes_prepared.all())
        response = self.client.get(
            reverse("kitchen:toggle-dish-assign", args=[self.dish2.id])
        )
        self.assertRedirects(
            response,
            reverse("kitchen:dish-detail", args=[self.dish2.id])
        )
        self.cook1.refresh_from_db()
        self.assertNotIn(self.dish2, self.cook1.dishes_prepared.all())

    def test_cook_create_view(self):
        response = self.client.get(reverse("kitchen:cook-create"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:cook-create"),
            {
                "username": "newchef",
                "first_name": "New",
                "last_name": "Chef",
                "years_of_experience": 3,
                "email": "newchef@test.com",
                "password1": "securepassword123",
                "password2": "securepassword123",
            },
        )
        self.assertRedirects(response, reverse("kitchen:cook-list"))
        self.assertTrue(Cook.objects.filter(username="newchef").exists())

    def test_cook_update_view(self):
        response = self.client.get(
            reverse("kitchen:cook-update", args=[self.cook1.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:cook-update", args=[self.cook1.id]),
            {"years_of_experience": 12}
        )
        self.assertRedirects(response, reverse("kitchen:cook-list"))
        self.cook1.refresh_from_db()
        self.assertEqual(self.cook1.years_of_experience, 12)

    def test_cook_delete_view(self):
        response = self.client.get(
            reverse("kitchen:cook-delete", args=[self.cook2.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:cook-delete", args=[self.cook2.id])
        )
        self.assertRedirects(response, reverse("kitchen:cook-list"))
        self.assertFalse(Cook.objects.filter(id=self.cook2.id).exists())

    def test_dish_type_create_view(self):
        response = self.client.get(reverse("kitchen:dish-type-create"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:dish-type-create"),
            {"name": "Dessert"}
        )
        self.assertRedirects(response, reverse("kitchen:dish-type-list"))
        self.assertTrue(DishType.objects.filter(name="Dessert").exists())

    def test_dish_type_update_view(self):
        response = self.client.get(
            reverse("kitchen:dish-type-update", args=[self.dish_type1.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:dish-type-update", args=[self.dish_type1.id]),
            {"name": "Appetizer Updated"}
        )
        self.assertRedirects(response, reverse("kitchen:dish-type-list"))
        self.dish_type1.refresh_from_db()
        self.assertEqual(self.dish_type1.name, "Appetizer Updated")

    def test_dish_type_delete_view(self):
        response = self.client.get(
            reverse("kitchen:dish-type-delete", args=[self.dish_type2.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:dish-type-delete", args=[self.dish_type2.id])
        )
        self.assertRedirects(response, reverse("kitchen:dish-type-list"))
        self.assertFalse(
            DishType.objects.filter(id=self.dish_type2.id).exists()
        )

    def test_dish_create_view(self):
        response = self.client.get(reverse("kitchen:dish-create"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:dish-create"),
            {
                "name": "New Dish",
                "description": "New description",
                "price": "20.00",
                "dish_type": self.dish_type1.id,
                "cooks": [self.cook1.id],
                "ingredients": [self.ingredient1.id],
            },
        )
        self.assertRedirects(response, reverse("kitchen:dish-list"))
        self.assertTrue(Dish.objects.filter(name="New Dish").exists())

    def test_dish_update_view(self):
        response = self.client.get(
            reverse("kitchen:dish-update", args=[self.dish1.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:dish-update", args=[self.dish1.id]),
            {
                "name": "Updated Bruschetta",
                "description": "Updated description",
                "price": "15.00",
                "dish_type": self.dish_type1.id,
                "cooks": [self.cook1.id],
                "ingredients": [self.ingredient1.id],
            },
        )
        self.assertRedirects(response, reverse("kitchen:dish-list"))
        self.dish1.refresh_from_db()
        self.assertEqual(self.dish1.name, "Updated Bruschetta")

    def test_dish_delete_view(self):
        response = self.client.get(
            reverse("kitchen:dish-delete", args=[self.dish3.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:dish-delete", args=[self.dish3.id])
        )
        self.assertRedirects(response, reverse("kitchen:dish-list"))
        self.assertFalse(Dish.objects.filter(id=self.dish3.id).exists())

    def test_ingredient_create_view(self):
        response = self.client.get(reverse("kitchen:ingredient-create"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:ingredient-create"),
            {"name": "Garlic"}
        )
        self.assertRedirects(response, reverse("kitchen:ingredient-list"))
        self.assertTrue(Ingredient.objects.filter(name="Garlic").exists())

    def test_ingredient_update_view(self):
        response = self.client.get(
            reverse("kitchen:ingredient-update", args=[self.ingredient1.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:ingredient-update", args=[self.ingredient1.id]),
            {"name": "Tomato Updated"}
        )
        self.assertRedirects(response, reverse("kitchen:ingredient-list"))
        self.ingredient1.refresh_from_db()
        self.assertEqual(self.ingredient1.name, "Tomato Updated")

    def test_ingredient_delete_view(self):
        response = self.client.get(
            reverse("kitchen:ingredient-delete", args=[self.ingredient2.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("kitchen:ingredient-delete", args=[self.ingredient2.id])
        )
        self.assertRedirects(response, reverse("kitchen:ingredient-list"))
        self.assertFalse(
            Ingredient.objects.filter(id=self.ingredient2.id).exists()
        )

    def test_cook_ordering(self):
        cooks = Cook.objects.filter(
            username__in=[self.cook1.username, self.cook2.username]
        )
        self.assertEqual(
            list(cooks),
            sorted(cooks, key=lambda c: c.username)
        )

    def test_dish_ordering(self):
        dishes = Dish.objects.all()
        self.assertEqual(
            list(dishes),
            sorted(dishes, key=lambda d: d.name)
        )

    def test_ingredient_ordering(self):
        ingredients = Ingredient.objects.all()
        self.assertEqual(
            list(ingredients),
            sorted(ingredients, key=lambda i: i.name)
        )

    def test_cook_detail_view(self):
        response = self.client.get(
            reverse("kitchen:cook-detail", kwargs={"pk": self.cook1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cook1.username)

    def test_dish_detail_view(self):
        response = self.client.get(
            reverse("kitchen:dish-detail", kwargs={"pk": self.dish1.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dish1.name)

    def test_ingredient_detail_view(self):
        response = self.client.get(
            reverse(
                "kitchen:ingredient-detail",
                kwargs={"pk": self.ingredient1.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.ingredient1.name)

    def test_cook_pagination(self):
        for i in range(3, 8):
            Cook.objects.create_user(
                username=f"pagi-chef{i}", password="secret"
            )
        response = self.client.get(reverse("kitchen:cook-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["cook_list"]), 5)
        response2 = self.client.get(reverse("kitchen:cook-list") + "?page=2")
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, "pagi-chef6")
        self.assertContains(response2, "pagi-chef7")

    def test_cook_pagination_preserves_search_params(self):
        for i in range(6):
            Cook.objects.create_user(
                username=f"pgsearch{i}", password="secret"
            )
        response = self.client.get(
            reverse("kitchen:cook-list") + "?username=pgsearch&page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "username=pgsearch")
