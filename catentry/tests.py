from django.test import TestCase
from django.urls import reverse
from .models import Cat, Adopter

# Create your tests here.


class CatModelTest(TestCase):
    def test_cat_creation(self):
        cat = Cat.objects.create(cat_name="Test Cat")
        self.assertEqual(cat.__str__(), "Test Cat - 1")

class AdopterModelTest(TestCase):
    def test_adopter_creation(self):
        cat = Cat.objects.create(cat_name="Test Cat")
        adopter = Adopter.objects.create(cat=cat, adopter_name="Test Adopter")
        self.assertEqual(adopter.__str__(), "Test Adopter - Test Cat")

class CatViewTest(TestCase):
    def test_cat_list_view(self):
        response = self.client.get(reverse("cat-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No cats are available.")

    def test_cat_detail_view(self):
        cat = Cat.objects.create(cat_name="Test Cat")
        response = self.client.get(reverse("cat-detail", args=[cat.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Cat")


class AdopterViewTest(TestCase):
    def test_adopter_list_view(self):
        response = self.client.get(reverse("adopter-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No adopters are available.")

    def test_adopter_detail_view(self):
        cat = Cat.objects.create(cat_name="Test Cat")
        adopter = Adopter.objects.create(cat=cat, adopter_name="Test Adopter")
        response = self.client.get(reverse("adopter-detail", args=[adopter.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Adopter")
