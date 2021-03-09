from collections import OrderedDict
from http import HTTPStatus

from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from mock import Mock, patch
from rest_framework.test import APIRequestFactory

from .factories import TaskFactory
from .models import Task, TaskStatusChoices
from .tasks import generate_random_number
from .views import TaskViewset


class TestTaskModel(TestCase):
    def setUp(self):
        self.name = "testing task model 1"

    def test_str(self):
        self.assertEqual(str(TaskFactory(name=self.name)), self.name)

    def test_is_available(self):
        self.assertTrue(Task.is_available())
        TaskFactory(name=self.name)
        self.assertFalse(Task.is_available())


class TestTaskViewset(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.endpoint = "/tasks/"
        self.view = TaskViewset
        self.name = "testing task viewset 1"
        self.proc_id = "testing proc id"
        self.task_mock = Mock()
        self.task_mock.apply_async.return_value = Mock(id=self.proc_id)
        self.patcher = patch.multiple(
            "api.views", generate_random_number=self.task_mock
        )

        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_create(self):
        options = {"data": {"name": self.name}, "format": "json"}
        req = self.factory.post(self.endpoint, **options)
        resp = self.view.as_view({"post": "create"})(req)

        self.assertEqual(resp.status_code, HTTPStatus.CREATED)
        self.assertEqual(resp.data, options["data"])
        self.task_mock.apply_async.assert_called_once_with(args=(self.name,))
        self.assertEqual(Task.objects.get(name=self.name).proc_id, self.proc_id)

    def test_create_task_already_exists(self):
        options = {"data": {"name": self.name}, "format": "json"}
        req = self.factory.post(self.endpoint, **options)
        resp = self.view.as_view({"post": "create"})(req)
        req = self.factory.post(self.endpoint, **options)
        resp = self.view.as_view({"post": "create"})(req)
        message = _("task with this name already exists.")

        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(str(resp.data.get("name", [""])[-1]), message)
        self.task_mock.apply_async.assert_called_once_with(args=(self.name,))

    def test_create_task_while_in_progress(self):
        options = {"data": {"name": self.name}, "format": "json"}
        req = self.factory.post(self.endpoint, **options)
        resp = self.view.as_view({"post": "create"})(req)
        options["data"]["name"] = "new task 1"
        req = self.factory.post(self.endpoint, **options)
        resp = self.view.as_view({"post": "create"})(req)
        message = _("Another task is in progress, try again later.")

        self.assertEqual(resp.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertEqual(resp.data.get("detail", ""), message)
        self.task_mock.apply_async.assert_called_once_with(args=(self.name,))

    def test_list_tasks(self):
        task = TaskFactory(name=self.name)
        req = self.factory.get(self.endpoint)
        resp = self.view.as_view({"get": "list"})(req)
        serialized = OrderedDict([("name", task.name), ("status", task.status)])

        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.data, [serialized])

    def test_retrieve_task(self):
        task = TaskFactory(name=self.name)
        req = self.factory.get(self.endpoint)
        resp = self.view.as_view({"get": "retrieve"})(req, name=self.name)
        serialized = {"name": task.name, "status": task.status}

        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.data, serialized)


class TestTasks(TestCase):
    def setUp(self):
        self.name = "testing tasks 1"
        self.mock_time = Mock()
        self.patcher = patch.multiple("api.tasks", time=self.mock_time)

        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_generate_random_number(self):
        task = TaskFactory(name=self.name)
        prev_status, prev_result = task.status, task.result
        generate_random_number(task_name=self.name)
        task = Task.objects.get(pk=task.pk)

        self.mock_time.sleep.assert_called_once_with(100)
        self.assertEqual(prev_status, TaskStatusChoices.IN_PROGRESS)
        self.assertEqual(task.status, TaskStatusChoices.COMPLETE)
        self.assertIsNone(prev_result)
        self.assertIsInstance(task.result, int)
