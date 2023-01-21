import unittest, os


class BaseRedisTaskTest(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

        os.environ['REDIS_HOST'] = 'localhost'
        os.environ['REDIS_PORT'] = '6379'
        os.environ['REDIS_TTL'] = '60'