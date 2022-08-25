'''
    Set a connection string and database name in the environment.
    Preferably using a .env file.
'''
import unittest
from dotenv import load_dotenv

load_dotenv('.env')

# Import the base mongo model
from traducteur import BaseMongoModel

# User class for testing

class User(BaseMongoModel):
    username: str
    fname: str
    lname: str
    email: str

# test class
class TestCRUDMethods(unittest.TestCase):
    def setUp(self):
        self.user = User(
            username='johndoe',
            fname='John',
            lname='Doe',
            email='john.doe@mail.com'
        )

    def test_save(self):
        user = self.user.save()

        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertIsNotNone(user.id, 'user.id is not set or not getable')
        self.assertIsNotNone(user.created_at, 'user.created_at is not set or getable')

    def test_get(self):
        user_id = self.user.save().id
        newuser = User.get(user_id)

        self.assertIsNotNone(newuser, 'could not get user')
        self.assertEqual(user_id, newuser.id, 'user ids not equal')

    def test_update(self):
        user = self.user.save()
        user.fname = 'Sam'
        update = user.save()

        self.assertEqual(update.fname, 'Sam', 'First name not updated')
        self.assertEqual(str(update.id), str(user.id), 'Original and updated ids are not equal')

    def test_delete(self):
        user = self.user.save()
        self.assertIsNotNone(User.get(user.id))
        user.delete()
        self.assertIsNone(User.get(user.id))


if __name__ == '__main__':
    unittest.main()