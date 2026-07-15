from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages


class UserCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
        }
        self.existing_user = User.objects.create_user(
            username='existing',
            password='ExistingPass123!'
        )

    def test_user_registration(self):
        """Тест регистрации нового пользователя"""
        response = self.client.post(
            reverse('user_create'),
            self.user_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testuser').exists())

        # Проверка сообщения
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно зарегистрирован')

        # Проверка редиректа на страницу входа
        self.assertRedirects(response, reverse('login'))

    def test_user_registration_with_existing_username(self):
        """Тест регистрации с существующим именем пользователя"""
        data = self.user_data.copy()
        data['username'] = 'existing'
        response = self.client.post(
            reverse('user_create'),
            data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        # Проверка, что пользователь не создан
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_user_login(self):
        """Тест входа пользователя"""
        # Сначала создаем пользователя
        self.client.post(reverse('user_create'), self.user_data)

        # Вход
        response = self.client.post(
            reverse('login'),
            {
                'username': 'testuser',
                'password': 'TestPassword123!'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы залогинены')

    def test_user_logout(self):
        """Тест выхода пользователя"""
        # Создаем и логиним пользователя
        user = User.objects.create_user(
            username='testuser2',
            password='TestPass123!'
        )
        self.client.login(username='testuser2', password='TestPass123!')

        # Выход
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        # Проверяем наличие сообщения о выходе
        self.assertTrue(any('разлогинены' in str(msg) for msg in messages))

    def test_user_update(self):
        """Тест обновления пользователя"""
        # Создаем и логиним пользователя
        user = User.objects.create_user(
            username='testuser3',
            password='TestPass123!',
            first_name='Old',
            last_name='Name'
        )
        self.client.login(username='testuser3', password='TestPass123!')

        # Обновление
        response = self.client.post(
            reverse('user_update', args=[user.pk]),
            {
                'username': 'testuser3',
                'first_name': 'New',
                'last_name': 'Name'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'New')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно изменен')

    def test_user_update_by_other_user(self):
        """Тест обновления пользователя другим пользователем"""
        # Создаем двух пользователей
        user1 = User.objects.create_user(
            username='user1',
            password='Pass123!'
        )
        user2 = User.objects.create_user(
            username='user2',
            password='Pass123!'
        )
        self.client.login(username='user2', password='Pass123!')

        # Попытка обновить user1
        response = self.client.post(
            reverse('user_update', args=[user1.pk]),
            {
                'username': 'user1',
                'first_name': 'Hacked',
                'last_name': 'User'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'У вас нет прав для изменения')

    def test_user_delete(self):
        """Тест удаления пользователя"""
        # Создаем и логиним пользователя
        user = User.objects.create_user(
            username='testuser4',
            password='TestPass123!'
        )
        self.client.login(username='testuser4', password='TestPass123!')

        # Удаление
        response = self.client.post(
            reverse('user_delete', args=[user.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser4').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно удален')

    def test_user_delete_by_other_user(self):
        """Тест удаления пользователя другим пользователем"""
        user1 = User.objects.create_user(
            username='user1',
            password='Pass123!'
        )
        user2 = User.objects.create_user(
            username='user2',
            password='Pass123!'
        )
        self.client.login(username='user2', password='Pass123!')

        # Попытка удалить user1
        response = self.client.post(
            reverse('user_delete', args=[user1.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='user1').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'У вас нет прав для изменения')

    def test_users_list(self):
        """Тест списка пользователей"""
        # Создаем несколько пользователей
        User.objects.create_user(username='user1', password='Pass123!')
        User.objects.create_user(username='user2', password='Pass123!')

        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user1')
        self.assertContains(response, 'user2')
