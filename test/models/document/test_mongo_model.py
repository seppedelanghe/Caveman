import unittest
from traducteur.models.document.mongo import BaseMongoModel


# User class for testing
class User(BaseMongoModel):
    username: str
    fname: str
    lname: str
    email: str


# test class
class TestCRUDMethods(unittest.TestCase):
    def setUp(self):
        """
            Set a connection string and database name in the environment.
        """
        # import os
        # os.environ['MONGO_CONNECTION_STR'] = ''
        # os.environ['MONGO_DATABASE_NAME'] = ''

        self.user = User(
            username='johndoe',
            fname='John',
            lname='Doe',
            email='john.doe@mail.com'
        )

    def test_mongo_model_can_save(self):
        user = self.user.save()

        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertIsNotNone(user.id, 'user.id is not set or not getable')
        self.assertIsNotNone(user.created_at, 'user.created_at is not set or getable')

    def test_mongo_model_can_get(self):
        user = self.user.save()
        user_id = user.id
        new_user = User.get(user_id)

        self.assertIsNotNone(new_user, 'could not get user')
        self.assertEqual(user_id, new_user.id, 'user ids not equal')

    def test_mongo_model_can_get_all(self):
        self.user.save()

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

        items = User.all(limit=3)

        self.assertIsNotNone(items, 'could not get all items')
        self.assertTrue(len(items) > 0, 'items is a list but is empty')

    def test_mongo_model_can_update(self):
        user = self.user.save()
        user.fname = 'Sam'
        update = user.save()

        self.assertEqual(update.fname, 'Sam', 'First name not updated')
        self.assertEqual(str(update.id), str(user.id), 'Original and updated ids are not equal')

    def test_mongo_model_can_delete(self):
        user = self.user.save()
        self.assertIsNotNone(User.get(user.id))
        user.delete()
        self.assertIsNone(User.get(user.id))
