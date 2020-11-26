"""
API V1: Test Topics
"""
###
# Libraries
###
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


User = get_user_model()


###
# Test Cases
###
class TopicsTestCase(APITestCase):
    def setUp(self):
        self.password = 'testuser'
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
        )
        self.user.set_password(self.password)
        self.user.save()
        Token.objects.create(user=self.user)

        self.user2 = User.objects.create(
            username='testuser2',
            email='testuser2@example.com',
        )
        self.user2.set_password(self.password)
        self.user2.save()
        Token.objects.create(user=self.user2)

    def test_create_topic(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        url = reverse('topics-list')
        payload = {
            'name': 'Python topic',
            'title': 'PythonDevs',
            'description': 'Python forum for Devs',
            'url_name': 'python',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data['author'], self.user.id)

    def test_list_topic(self):
        url = reverse('topics-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        payload = {
            'name': 'Python topic',
            'title': 'PythonDevs',
            'description': 'Python forum for Devs',
            'url_name': 'python',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2.auth_token.key)
        payload = {
            'name': 'Node Topic',
            'title': 'Node devs',
            'description': 'Node forum for Devs',
            'url_name': 'nodejs',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.get(url)
        self.assertEqual(res.data['count'], 2)

    def test_update_topic(self):
        url = reverse('topics-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        old_name = 'python'
        payload = {
            'name': old_name,
            'title': 'PythonDevs',
            'description': 'Python forum for Devs',
            'url_name': 'python',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('topics-detail', kwargs={'url_name': payload['url_name']})
        new_name = 'python2'
        payload['name'] = new_name

        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_name)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2.auth_token.key)
        payload['name'] = old_name
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token fdaf@invalido0sas')
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_url_name_topic(self):
        url = reverse('topics-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        old_name = 'python'
        payload = {
            'name': 'Python topic',
            'title': 'PythonDevs',
            'description': 'Python forum for Devs',
            'url_name': old_name,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('topics-detail', kwargs={'url_name': payload['url_name']})
        new_name = 'python2'
        payload['url_name'] = new_name

        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_topic(self):
        url = reverse('topics-list')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        payload = {
            'name': 'python',
            'title': 'PythonDevs',
            'description': 'Python forum for Devs',
            'url_name': 'python',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('topics-detail', kwargs={'url_name': payload['url_name']})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2.auth_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token fdaf@invalido0sas')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse('topics-list'))
        self.assertEqual(response.data['count'], 0)
