import unittest
from traducteur.models.base import BaseDatabaseModel


# test class
class TestBaseModel(unittest.TestCase):
    def test_model_uuids_are_unique(self):
        a = BaseDatabaseModel()
        b = BaseDatabaseModel()
        c = BaseDatabaseModel()

        self.assertNotEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(b, c)
