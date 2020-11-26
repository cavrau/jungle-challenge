"""
API V1: Test Comments
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
from posts.models import Post

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
        self.p1 = Post.objects.create(title='Python', content='lorem ipsum', author=self.user, topic=self.t1)
        self.p2 = Post.objects.create(title='Django', content='lorem ipsum', author=self.user2, topic=self.t1)
        self.p3 = Post.objects.create(title='Node', content='lorem ipsum', author=self.user, topic=self.t2)
        self.p4 = Post.objects.create(title='Express', content='lorem ipsum', author=self.user2, topic=self.t2)

    def test_create_comment(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        url = reverse('comments-list', kwargs={'topic_pk': 'python', 'post_pk': 1})
        payload = {
            'title': 'I disagree Flask is better',
            'content': 'Lorem ipsum sid dolor at met',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data['author'], self.user.id)

    def test_create_comment_wrong_topic(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        url = reverse('comments-list', kwargs={'topic_pk': 'jedi', 'post_pk': 1})
        payload = {
            'title': 'I disagree Flask is better',
            'content': 'Lorem ipsum sid dolor at met',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_post(self):
        url = reverse('comments-list', kwargs={'topic_pk': 'python', 'post_pk': self.p1.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        payload = {
            'title': 'Python is the best',
            'content': 'Python is the best and django is better',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = reverse('comments-list', kwargs={'topic_pk': 'python', 'post_pk': self.p2.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2.auth_token.key)
        payload = {
            'title': 'Django is the best',
            'content': 'Django is the best and flask is better',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials(HTTP_AUTHORIZATION='')
        res = self.client.get(url)
        self.assertEqual(res.data['count'], 1)
        url = reverse('comments-list', kwargs={'topic_pk': 'python', 'post_pk': self.p1.pk})
        res = self.client.get(url)
        self.assertEqual(res.data['count'], 1)

    def test_update_topic(self):
        url = reverse('comments-list', kwargs={'topic_pk': 'python', 'post_pk': self.p2.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        old_title = 'Django is the best'
        payload = {
            'title': old_title,
            'content': 'Django is the best and flask is better',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse(
            'comments-detail',
            kwargs={'topic_pk': 'python', 'post_pk': self.p2.pk, 'pk': response.data['id']}
        )
        new_title = 'Flask is the best'
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
        url = reverse('comments-list', kwargs={'topic_pk': 'python', 'post_pk': self.p2.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        payload = {
            'title': 'Python is the best',
            'content': 'Python is the best and django is better',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse(
            'comments-detail',
            kwargs={'topic_pk': 'python', 'post_pk': self.p2.pk, 'pk': response.data['id']}
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2.auth_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.credentials(HTTP_AUTHORIZATION='Token fdaf@invalido0sas')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        url = reverse('comments-list', kwargs={'topic_pk': 'python', 'post_pk': self.p2.pk})

        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 0)
