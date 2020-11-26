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

from topics.models import Topic

User = get_user_model()


###
# Test Cases
###
class PostsTestCase(APITestCase):
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
        self.t1 = Topic.objects.create(
            name='Python',
            title='PythonDevs',
            description='Python Forum',
            url_name='python',
            author=self.user
        )
        self.t2 = Topic.objects.create(
            name='Node',
            title='NodeDevs',
            description='Node Forum',
            url_name='nodejs',
            author=self.user2
        )

    def test_create_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        url = reverse('posts-list', kwargs={'topic_pk': 'python'})
        payload = {
            'title': 'Python is the best',
            'content': 'Python is the best and django is better',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data['author'], self.user.id)

    def test_create_title_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        url = reverse('posts-list', kwargs={'topic_pk': 'python'})
        payload = {
            'title': 'Python is the best',
            'content': 'Python is the best and django is better',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(reverse('posts-list', kwargs={'topic_pk': 'nodejs'}), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_post(self):
        url = reverse('posts-list', kwargs={'topic_pk': 'python'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        payload = {
            'title': 'Python is the best',
            'content': 'Python is the best and django is better',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('posts-list', kwargs={'topic_pk': 'nodejs'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2.auth_token.key)
        payload = {
            'title': 'Node is the best',
            'content': 'Node is the best and express is better',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.get(url)
        self.assertEqual(res.data['count'], 1)
        url = reverse('posts-list', kwargs={'topic_pk': 'python'})
        res = self.client.get(url)
        self.assertEqual(res.data['count'], 1)

    def test_update_topic(self):
        url = reverse('posts-list', kwargs={'topic_pk': 'python'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        old_title = 'Python is the best'
        payload = {
            'title': old_title,
            'content': 'Node is the best and express is better',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('posts-detail', kwargs={'topic_pk': 'python', 'pk': response.data['id']})
        new_title = 'Django is the best'
        payload['title'] = new_title

        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], new_title)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2.auth_token.key)
        payload['title'] = old_title
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token fdaf@invalido0sas')
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_topic(self):
        url = reverse('posts-list', kwargs={'topic_pk': 'python'})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        payload = {
            'title': 'Python is the best',
            'content': 'Python is the best and django is better',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('posts-detail', kwargs={'topic_pk': 'python', 'pk': response.data['id']})

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2.auth_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token fdaf@invalido0sas')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(reverse('posts-list', kwargs={'topic_pk': 'python'}))
        self.assertEqual(response.data['count'], 0)
