import unittest
from traducteur.models.document.mongo import BaseMongoModel


# User class for testing
class User(BaseMongoModel):
    username: str
    fname: str
    lname: str
    email: str


class TestManyMethods(unittest.TestCase):
    def setUp(self):
        self.user1 = User(
            username='johndoe',
            fname='John',
            lname='Doe',
            email='john.doe@mail.com'
        ).save()

        self.user2 = User(
            username='adamsandler',
            fname='Adam',
            lname='Sandler',
            email='adam.sandler@mail.com'
        ).save()

        self.user3 = User(
            username='tomhanks',
            fname='Tom',
            lname='Hanks',
            email='tom.hanks@mail.com'
        ).save()

    def test_limit(self):
        users = User.all(limit=2)

        self.assertIsNotNone(users, 'users is empty')
        self.assertTrue(len(users) == 2, 'users is not limited')

    def test_sort(self):
        users = User.all(sort='fname')

        self.assertIsNotNone(users, 'users is empty')
        self.assertTrue(users[0].fname == 'Adam', 'users not sorted by fname')

    def test_sort_desc(self):
        users = User.all(sort='fname', sortdirection=-1)

        self.assertIsNotNone(users, 'users is empty')
        self.assertTrue(users[0].fname == 'Tom', 'users not sorted descending by fname')
