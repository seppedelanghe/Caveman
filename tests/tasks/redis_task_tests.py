import unittest
import os

from traducteur.tasks.task import RedisTask
from traducteur.tasks.base.status import TaskStatus

def test_action(**kwargs) -> dict:
    return {
        'math': 1 + 2
    }

class RedisTaskTests(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        os.environ['REDIS_HOST'] = 'localhost'
        os.environ['REDIS_PORT'] = '6379'
        os.environ['REDIS_TTL'] = '60'

        self.task = RedisTask(channel='some-channel', action=test_action)

    def test_task_can_be_created(self):
        self.assertIsInstance(self.task, RedisTask)

    def test_task_can_be_queued_without_parameters(self):
        self.task.queue()

    def test_task_cannot_be_queued_with_parameter(self):
        self.assertRaises(TypeError, self.task.queue, (3))

    def test_task_can_be_queued_with_named_parameter(self):
        self.task.queue(param=3)

    def test_task_can_be_digested(self):
        self.task.digest()

    def test_task_has_output(self):
        self.task.queue()
        self.task.digest()
        
        out = self.task.tout

        self.assertIsNotNone(out)
        self.assertIsInstance(out, dict)
        self.assertDictEqual(out, {
            'math': 3
        })

    def test_task_saves_input(self):
        self.task.queue(param=4)
        
        self.assertIsNotNone(self.task.tin)
        self.assertIsInstance(self.task.tin, dict)
        self.assertDictEqual(self.task.tin, {
            'param': 4
        })

    def test_task_can_get_status(self):
        self.assertEqual(self.task.status, TaskStatus.NONE)
        
        self.task.queue()
        self.assertEqual(self.task.status, TaskStatus.QUEUED)

        self.task.digest()
        self.assertEqual(self.task.status, TaskStatus.SUCCEEDED)