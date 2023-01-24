# Traducteur
Traducteur is a database model manager and task sheduler which aims to make developing basic app with database models and tasks faster and easier.


<div align="center">
    <img src="https://img.shields.io/pypi/v/traducteur"/>
    <img src="https://img.shields.io/pypi/dm/traducteur"/>
    <img src="https://img.shields.io/github/actions/workflow/status/seppedelanghe/traducteur/tests.yaml?label=tests" />
    <br/>
    <img src="https://img.shields.io/pypi/pyversions/traducteur"/>
    <img src="https://img.shields.io/github/languages/code-size/seppedelanghe/traducteur"/>
</div>

## Requirements
- `python ^3.8`
- `pydantic ^1.10.4`

### Optional
__For mongo db:__
- `pymongo ^4.3.3`

__For task queueing or redis model management:__
- `redis-py ^4.4.2`

## Installation
__Base install:__
```
pip install traducteur
```

__Install with extras:__
```
pip install "traducteur[tasks]"
```
This example will install traducteur and all the packages you need to use traducteur tasks.

__optional extras:__
- sql
- nosql
- caching
- mongo
- tasks
- all


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
result = manager.get(example_id)
result = manager.delete(example_id)
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

### Chain tasks
Tasks can be chained together for larger workloads
```python
def double(number: int):
    return {
        'number': number * 2
    }

# make tasks
one = BaseTask(action=double)
two = BaseTask(action=double)
three = BaseTask(action=double)

# chain tasks
two.set_parent(one)
three.set_parent(two)

# queue parent task
one.queue(number=2)

###############
# in a worker #
one.digest()  #
###############

# some time later
result = one.result()
assert result == 8, "Should be 8 as 2*2*2 == 8"
```

## Available functionality

### Context managers
- MongoContext
- SQLite3Context


### Model managers
- MongoModelManager
- SQLModelManager
  - SQLQueryBuilder

### Query filters
- Datetime filter
- Number filter
- String filter

### Models
- BaseMongoModel
- BaseRedisModel
- BaseSQLModel

### Tasks
- RedisTask

# Todo / in progress

### Tasks
- [ ] Chain tasks
    - [x] Redis
    - [ ] Mongo
    - [ ] SQL
- [ ] Task worker
  	- [ ] Single Process
    - [ ] Multi Process
- [ ] RabbitMQ task

# Tests

Tests can be found in the `test` folder. They use pythons `unittest` and can be run with:
```
python3 -m unittest path/to/test.py
```

Tests get automatically run after each push.

### Available tests
- Mongo model
- Mongo sorting
- Redis task
    - Basic functions
    - Chaining