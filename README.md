# Traducteur
Traducteur is a database model manager and task sheduler which aims to make developing basic app with database models and tasks faster and easier.

## Requirements
- `python ^3.8`
- `pydantic ^1.10.4`

__For mongo db management:__
- `pymongo ^4.3.3`

__For task queueing or redis model management:__
- `redis-py ^4.4.2`

## The idea

### Context managers
```python
with BaseContext(connection_string) as db:
    return db.get()
```

### Model managers
Model managers use context managers
```python
manager = BaseModelManager(connection_string)
result = manager.find_one(query)
result = manager.delete(query)
```

### Models
Models use model managers
```python
class User(BaseDatabaseModel):
    username: str
    fname: str
    lname: str
    email: str
    
user = User(
    username='johndoe',
    fname='John',
    lname='Doe',
    email='john.doe@mail.com'
)

'''
    Easy create, save, update and delete
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
user.lname = 'Joe'
user = user.save()

# getting a model by its ID from the database
user = User.get(user_id)

# deleting a model from the database
deleted_user = user.delete()
```

### Tasks
Tasks use models
```python
# in a program
def my_func(a: int, b: int) -> int:
  return a + b

task = BaseTask(action=my_func)
task.queue(a=8, b=3)

###############
# in a worker #
task.digest() #
###############

# some time later
result = task.result()
```

## Available functionality

### Context managers
- MongoContext
- SQLite3Context


### Model managers
- MongoModelManager

### Models
- BaseMongoModel
- BaseRedisModel

### Tasks
- RedisTask

## Todo

### Models
- [ ] SQLite support

### Tasks
- [ ] Task chains
    - synchronous
    - asynchronous
- [ ] Task worker
  	- Single Process
    - Multi Process
- [ ] RabbitMQ task

### Managers
- [ ] SQLite manager
