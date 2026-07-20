from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from task_manager.models import Status, Task, Label


class UserCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.user_data = {
            'username': 'newuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'TestPassword123!',
            'password2': 'TestPassword123!',
        }

    def test_user_registration(self):
        """Тест регистрации"""
        response = self.client.post(reverse('user_create'), self.user_data, follow=True)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно зарегистрирован')
        self.assertRedirects(response, reverse('login'))

    def test_user_login(self):
        """Тест входа"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'TestPass123!',
        }, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Вы залогинены')

    def test_user_logout(self):
        """Тест выхода"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(reverse('logout'), follow=True)
        self.assertFalse('_auth_user_id' in self.client.session)


    def test_user_update(self):
        """Тест обновления пользователя"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(
            reverse('user_update', args=[self.user.pk]),
            {'username': 'testuser', 'first_name': 'NewName', 'last_name': 'User'},
            follow=True
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NewName')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно изменен')

    def test_user_delete(self):
        """Тест удаления пользователя"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(reverse('user_delete', args=[self.user.pk]), follow=True)
        self.assertFalse(User.objects.filter(username='testuser').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Пользователь успешно удален')


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.status = Status.objects.create(name='Existing Status')

    def test_status_list_requires_login(self):
        """Тест: список статусов требует авторизации"""
        response = self.client.get(reverse('statuses'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("statuses")}')

    def test_status_create(self):
        """Тест: создание статуса"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(
            reverse('status_create'),
            {'name': 'New Status'},
            follow=True
        )
        self.assertTrue(Status.objects.filter(name='New Status').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно создан')

    def test_status_update(self):
        """Тест: обновление статуса"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(
            reverse('status_update', args=[self.status.pk]),
            {'name': 'Updated Status'},
            follow=True
        )
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно изменен')

    def test_status_delete(self):
        """Тест: удаление статуса"""
        self.client.login(username='testuser', password='TestPass123!')
        status = Status.objects.create(name='To Delete')
        response = self.client.post(reverse('status_delete', args=[status.pk]), follow=True)
        self.assertFalse(Status.objects.filter(name='To Delete').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Статус успешно удален')


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='TestPass123!'
        )
        self.status = Status.objects.create(name='New')
        self.task = Task.objects.create(
            name='Existing Task',
            description='Existing Description',
            status=self.status,
            author=self.user,
            executor=self.user2
        )

    def test_task_list_requires_login(self):
        """Тест: список задач требует авторизации"""
        response = self.client.get(reverse('tasks'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("tasks")}')

    def test_task_create(self):
        """Тест: создание задачи"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(
            reverse('task_create'),
            {
                'name': 'New Task',
                'description': 'Test Description',
                'status': self.status.id,
                'executor': self.user2.id
            },
            follow=True
        )
        task = Task.objects.get(name='New Task')
        self.assertEqual(task.author, self.user)
        self.assertTrue(Task.objects.filter(name='New Task').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно создана')

    def test_task_update(self):
        """Тест: обновление задачи"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(
            reverse('task_update', args=[self.task.pk]),
            {'name': 'Updated Task',
             'status': self.status.id,
             'executor': self.user2.id
            },
            follow=True
        )
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно изменена')

    def test_task_delete_by_author(self):
        """Тест: удаление задачи автором"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]), follow=True)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задача успешно удалена')

    def test_task_delete_by_not_author(self):
        """Тест: удаление задачи не автором"""
        self.client.login(username='testuser2', password='TestPass123!')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]), follow=True)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задачу может удалить только ее автор')

    def test_task_detail(self):
        """Тест: просмотр задачи"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(reverse('task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Existing Task')

    class LabelCRUDTest(TestCase):
        def setUp(self):
            self.client = Client()
            self.user = User.objects.create_user(
                username='testuser',
                password='TestPass123!'
            )
            self.label_data = {
                'name': 'New Label'
            }
            self.label = Label.objects.create(name='Existing Label')

        def test_label_list_requires_login(self):
            """Тест: список меток требует авторизации"""
            response = self.client.get(reverse('labels'))
            self.assertRedirects(response, f'{reverse("login")}?next={reverse("labels")}')

        def test_label_create(self):
            """Тест: создание метки"""
            self.client.login(username='testuser', password='TestPass123!')
            response = self.client.post(
                reverse('label_create'),
                self.label_data,
                follow=True
            )
            self.assertTrue(Label.objects.filter(name='New Label').exists())
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(str(messages[0]), 'Метка успешно создана')

        def test_label_update(self):
            """Тест: обновление метки"""
            self.client.login(username='testuser', password='TestPass123!')
            response = self.client.post(
                reverse('label_update', args=[self.label.pk]),
                {'name': 'Updated Label'},
                follow=True
            )
            self.label.refresh_from_db()
            self.assertEqual(self.label.name, 'Updated Label')
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(str(messages[0]), 'Метка успешно изменена')

        def test_label_delete(self):
            """Тест: удаление метки"""
            self.client.login(username='testuser', password='TestPass123!')
            label = Label.objects.create(name='To Delete')
            response = self.client.post(
                reverse('label_delete', args=[label.pk]),
                follow=True
            )
            self.assertFalse(Label.objects.filter(name='To Delete').exists())
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(str(messages[0]), 'Метка успешно удалена')

        def test_label_delete_with_tasks(self):
            """Тест: удаление метки, связанной с задачей"""
            self.client.login(username='testuser', password='TestPass123!')
            status = Status.objects.create(name='New')
            label = Label.objects.create(name='In Use')
            task = Task.objects.create(
                name='Task with label',
                status=status,
                author=self.user,
                executor=self.user
            )
            task.labels.add(label)

            response = self.client.post(
                reverse('label_delete', args=[label.pk]),
                follow=True
            )
            self.assertTrue(Label.objects.filter(pk=label.pk).exists())
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(str(messages[0]), 'Невозможно удалить метку')


class TaskFilterTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123!'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='TestPass123!'
        )
        self.status1 = Status.objects.create(name='New')
        self.status2 = Status.objects.create(name='In Progress')
        self.label1 = Label.objects.create(name='Bug')
        self.label2 = Label.objects.create(name='Feature')

        self.task1 = Task.objects.create(
            name='Task 1',
            status=self.status1,
            author=self.user,
            executor=self.user
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Task 2',
            status=self.status2,
            author=self.user2,
            executor=self.user2
        )
        self.task2.labels.add(self.label2)

        self.task3 = Task.objects.create(
            name='Task 3',
            status=self.status1,
            author=self.user,
            executor=self.user2
        )

    def test_filter_by_status(self):
        """Тест: фильтрация по статусу"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(
            reverse('tasks'),
            {'status': self.status1.id}
        )
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 2)
        self.assertTrue(all(task.status == self.status1 for task in tasks))

    def test_filter_by_executor(self):
        """Тест: фильтрация по исполнителю"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(
            reverse('tasks'),
            {'executor': self.user2.id}
        )
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 2)
        self.assertTrue(all(task.executor == self.user2 for task in tasks))

    def test_filter_by_label(self):
        """Тест: фильтрация по метке"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(
            reverse('tasks'),
            {'labels': self.label1.id}
        )
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 1)
        self.assertTrue(self.label1 in tasks[0].labels.all())

    def test_filter_self_tasks(self):
        """Тест: фильтрация только своих задач"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(
            reverse('tasks'),
            {'self_tasks': 'on'}
        )
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 2)
        self.assertTrue(all(task.author == self.user for task in tasks))

    def test_filter_combined(self):
        """Тест: комбинированная фильтрация"""
        self.client.login(username='testuser', password='TestPass123!')
        response = self.client.get(
            reverse('tasks'),
            {
                'status': self.status1.id,
                'executor': self.user.id,
                'self_tasks': 'on'
            }
        )
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 1)
        task = tasks[0]
        self.assertEqual(task.status, self.status1)
        self.assertEqual(task.executor, self.user)
        self.assertEqual(task.author, self.user)
