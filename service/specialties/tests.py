from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .api.models import *


# Create your tests here.


class UniversitiesTest(APITestCase):
    """Class to test the University list endpoint"""
    def setUp(self):
        """set up test variables"""
        self.user = User.objects.create_user(username='example1234', password='strong_password')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.university = University.objects.create(name='university', slug='university', region='львів')

    def test_university_create(self):
        """Test creating"""
        data = {
            'name': 'NULP',
            'slug': 'nulp',
            'region': 'Львівська область',
        }
        response = self.client.post(reverse('university-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_university_list(self):
        """Test listing universities"""
        response = self.client.get(reverse('university-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UniversityDetailTest(APITestCase):
    """Class to test the University detail endpoint"""
    def setUp(self):
        """Set up test variables"""
        self.user = User.objects.create_user(username='example1234', password='strong_password')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.university = University.objects.create(name='University', slug='university', region='львів')

    def test_university_detail(self):
        """Test detail university"""
        response = self.client.get(reverse('university-detail', args=(self.university.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(University.objects.count(), 1)
        self.assertEqual(self.university.name, 'University')

    def test_university_delete(self):
        """Test delete university"""
        response = self.client.delete(reverse('university-detail', args=(self.university.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_university_put(self):
        """Test update university"""
        data = {
            'name': 'NULT',
            'slug': 'nult',
            'region': 'Львівська область',
        }
        response = self.client.put(reverse('university-detail', args=(self.university.id,)), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SpecialtyListTest(APITestCase):
    """Class to test the specialty list endpoint"""
    def setUp(self):
        """Set up test variables"""
        self.user = User.objects.create_user(username='example1234', password='strong_password')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_specialty_list(self):
        """Test specialty list"""
        response = self.client.get(reverse('specialty-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_specialty_create(self):
        """Test specialty create"""
        data = {
            "form_of_education": "Денна",
            "educational_degree": "Бакалавр (на основі Молодший спеціаліст)",
            "branch": " Управління та адміністрування",
            "number_of_spec": 71,
            "name_of_spec": " Управління та адміністрування",
            "faculty": "Null",
            "educational_program": "Освітня програма ",
            "offer_type": " Небюджетна Зарахування на 1 курс",
            "license_scope": 15,
            "contract": 15,
            "budget": 0,
            "average_contract_mark": 0.0,
            "average_budget_mark": 135.68,
            "university": 2,
            "time_of_study": 21,
            "examination_coefficients": {
                "Мотиваційний лист": "0.00"
            },
            "slug": "071-upravlinnja-ta-administruvannja",
            "characteristic": "Спеціальність ",
            "future": "Випускники",
        }
        response = self.client.post(reverse('specialty-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SpecialtyDetailTest(APITestCase):
    """Class to test the specialty detail endpoint"""
    def setUp(self):
        """Set up test variables"""
        self.user = User.objects.create_user(username='example1234', password='strong_password')
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.university = University.objects.create(name='university', slug='university', region='львів')
        self.specialty = Specialty.objects.create(
            form_of_education='Денна',
            educational_degree='1',
            branch='гілка',
            number_of_spec=23,
            name_of_spec='грабіжник',
            faculty='державна адм',
            educational_program='Освітня програма',
            offer_type='Небюджетна Зарахування на 1 курс',
            license_scope=15,
            contract=15,
            budget=0,
            average_contract_mark=0.0,
            average_budget_mark=135.68,
            university=self.university,
            time_of_study=21,
            examination_coefficients={"Мотиваційний лист": "0.00"},
            slug='071-upravlinnja-ta-administruvannja',
            characteristic='Спеціальність',
            future='Випускники'
        )

    def test_specialty_detail(self):
        """test specialty detail"""
        response = self.client.get(reverse('university-detail', args=(self.university.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(University.objects.count(), 1)

    def test_specialty_delete(self):
        """test specialty deletion"""
        response = self.client.delete(reverse('university-detail', args=(self.university.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_specialty_put(self):
        """test specialty update"""
        data = {
            "form_of_education": "Денна",
            "educational_degree": "Бакалавр (на основі Молодший спеціаліст)",
            "branch": "Управління та адміністрування",
            "number_of_spec": 71,
            "name_of_spec": "Управління та адміністрування",
            "faculty": "Null",
            "educational_program": "Освітня програма",
            "offer_type": "Небюджетна Зарахування на 1 курс",
            "license_scope": 15,
            "contract": 15,
            "budget": 0,
            "average_contract_mark": 0.0,
            "average_budget_mark": 135.68,
            "university": self.university.id,
            "time_of_study": 21,
            "examination_coefficients": {
                "Мотиваційний лист": "0.00"
            },
            "slug": "071-upravlinnja-ta-administruvannja",
            "characteristic": "Спеціальність",
            "future": "Випускники"
        }
        response = self.client.put(reverse('university-detail', args=(self.university.id,)), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

