from unittest import TestCase

from holour import json_encode, json_decode
from holour.msg import Task


class Test(TestCase):

    def test_task(self):
        task = Task('uuid_1', 'task_1', ['task_2', 'task_3'], [])
        task_string = json_encode(task)
        expected_string = '{"_type": "task", "uuid": "uuid_1", "name": "task_1", "sub_tasks": ["task_2", "task_3"], ' \
                          '"operations": [], "execute_parallel": false, "description": ""}'

        assert type(task_string) == str
        assert task_string == expected_string, f"Expected {expected_string}, got: {task_string}"

        task_decoded = json_decode(task_string)
        assert type(task_decoded) == Task, f"Got: {type(task_decoded)}. Expected {Task}"
        assert task_decoded == task, "The decoded object must be equal to the encoded"

    def test_task_equals(self):
        t1 = Task('uuid_1', 'task_1', ['task_2', 'task_3'], [])
        t2 = Task('uuid_1', 'task_1', ['task_2', 'task_3'], [])
        t3 = Task('uuid_2', 'task_1', ['task_2', 'task_3'], [])

        assert t1 == t2
        assert t1 != t3
        assert t1 != "not status"

    def test_task_repr(self):
        task = Task('uuid_1', 'task_1', ['task_2', 'task_3'], [])
        expected, got = 'task_1', f'{task}'

        assert expected in got, f"Expected {expected} in got: {got}"

    def test_sub_tasks_or_operations(self):
        with self.assertRaises(ValueError):
            task = Task('uuid_1', 'task_1', [], [])
