# Traducteur

Traducteur is a pydantic model based database manager.
It currently only supports mongodb.

## Requirements

- `python >= 3.8` with:
    - `pymongo >= 4.0.1`
    - `pydantic >= 1.9.0`
    

## Example usage

```python
'''
    Set a connection string and database name in the environment.
    Preferably using a .env file.
'''
import os

CON_STR = 'mongodb://root:example@localhost:27017/'
DB_NAME = 'traducteur'

os.environ['TRADUCTEUR_CONNECTION_STR'] = CON_STR
os.environ['TRADUCTEUR_DATABASE'] = DB_NAME


'''
    Import the base model for the database you are using.
'''

from traducteur import BaseMongoModel

'''
    Make a model using the base model.
'''

class User(BaseMongoModel):
    username: str
    fname: str
    lname: str
    email: str

'''
    Easily create, save, update and delete the model
'''
user = User(
    username='johndoe',
    fname='John',
    lname='Doe',
    email='john.doe@mail.com'
)

# saving the model
user = user.save()

# saving also updates the model
user.lname = 'Doe updated'
user = user.save()

# save the user id and set user to None for the GET example
user_id = user.id
user = None

# getting a model by its ID from the database
user = User.get(user_id)
print(user.dict())

# deleting a model from the database
deleted_user = user.delete()
```