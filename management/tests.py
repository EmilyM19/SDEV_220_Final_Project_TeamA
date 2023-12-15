from django.test import TestCase
from django.urls import reverse
from .models import Cat, Adopter

class CatModelTest(TestCase):
    def setUp(self):
        Cat.objects.create(
            name='Fluffy',
            age=3,
            description='A cute and fluffy cat',
            spayed_neutered=True
        )

    def test_cat_name(self):
        cat = Cat.objects.get(id=1)
        self.assertEqual(cat.name, 'Fluffy')

    def test_cat_age(self):
        cat = Cat.objects.get(id=1)
        self.assertEqual(cat.age, 3)

    # Add more tests for other Cat model fields and methods as needed

class AdopterModelTest(TestCase):
    def setUp(self):
        Adopter.objects.create(
            name='John Doe',
            email='john@example.com',
            is_home_approved=True,
            adoption_complete=False
        )

    def test_adopter_name(self):
        adopter = Adopter.objects.get(id=1)
        self.assertEqual(adopter.name, 'John Doe')

    def test_adopter_email(self):
        adopter = Adopter.objects.get(id=1)
        self.assertEqual(adopter.email, 'john@example.com')


class CatListViewTest(TestCase):
    def test_cat_list_view_status_code(self):
        response = self.client.get(reverse('cat_list'))
        self.assertEqual(response.status_code, 200)

    def test_cat_list_view_uses_correct_template(self):
        response = self.client.get(reverse('cat_list'))
        self.assertTemplateUsed(response, 'cat_list.html')


class CatDetailViewTest(TestCase):
    def setUp(self):
        Cat.objects.create(
            name='Fluffy',
            age=3,
            description='A cute and fluffy cat',
            spayed_neutered=True
        )

    def test_cat_detail_view_status_code(self):
        response = self.client.get(reverse('cat_detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_cat_detail_view_uses_correct_template(self):
        response = self.client.get(reverse('cat_detail', args=[1]))
        self.assertTemplateUsed(response, 'cat_detail.html')