import redis, os, pickle

from .base_redis_test import BaseRedisTaskTest

from traducteur.tasks.task import RedisTask
from traducteur.tasks.base.status import TaskStatus

def test_action(**kwargs) -> dict:
    return {
        'number': kwargs.get('number', 2) * 2
    }

class ChainBuildingTests(BaseRedisTaskTest):
    def setUp(self) -> None:
        super().setUp()

        self.parent = RedisTask(channel='some-channel', action=test_action, id="uuid_1")
        self.child = RedisTask(channel='some-channel', action=test_action, id="uuid_2")
        self.child2 = RedisTask(channel='some-channel', action=test_action, id="uuid_3")

    def test_tasks_can_set_parent(self):
        self.child.set_parent(self.parent.id)

    def test_tasks_can_add_child(self):
        self.parent.add_child(self.child)

    def test_chained_tasks_can_be_queued(self):
        self.parent.add_child(self.child)
        self.child.set_parent(self.parent.id)

        # should queue parent and all children
        self.parent.queue()

        r = self.redis_instance()
        p = r.get(self.parent.id)
        c = r.get(self.child.id)

        # check
        self.assertIsNotNone(p)
        self.assertIsNotNone(c)

    def test_chained_tasks_can_be_unpickled(self):
        self.child.set_parent(self.parent.id)
        self.parent.add_child(self.child)
        
        # should queue parent and all children
        self.parent.queue()

        r = self.redis_instance()
        p: RedisTask = pickle.loads(r.get(self.parent.id))
        c: RedisTask = pickle.loads(r.get(self.child.id))

        # check
        self.assertIsInstance(p, RedisTask)
        self.assertIsInstance(c, RedisTask)

        self.assertEqual(p, self.parent)
        self.assertEqual(c, self.child)

    def test_chained_tasks_can_be_digested(self):
        self.parent.add_child(self.child)
        self.child.set_parent(self.parent.id)

        # should queue parent and all children
        self.parent.queue()
        self.parent.digest()

        # without worker => manual child digest
        self.child.digest()

        r = self.redis_instance()
        p: RedisTask = pickle.loads(r.get(self.parent.id))
        c: RedisTask = pickle.loads(r.get(self.child.id))

        self.assertEqual(p.status, TaskStatus.SUCCEEDED)
        self.assertEqual(c.status, TaskStatus.SUCCEEDED)

    def test_digest_chained_tasks_have_correct_outputs(self):
        self.parent.add_child(self.child)
        self.child.set_parent(self.parent.id)
        
        self.child.add_child(self.child2)
        self.child2.set_parent(self.child.id)

        # should queue parent and all children
        self.parent.queue()
        self.parent.digest()
        
        # without worker => manual child digest
        self.child.digest()
        self.child2.digest()

        r = self.redis_instance()
        p: RedisTask = pickle.loads(r.get(self.parent.id))
        c: RedisTask = pickle.loads(r.get(self.child.id))
        c2: RedisTask = pickle.loads(r.get(self.child2.id))

        self.assertEqual(p.tout, {
            'number': 2**2
        })

        self.assertEqual(c.tout, {
           'number': 2**3
        })

        self.assertEqual(c2.tout, {
           'number': 2**4
        })


    @staticmethod
    def redis_instance():
        return redis.Redis(host=os.environ.get('REDIS_HOST'), port=int(os.environ.get('REDIS_PORT', '6379')))