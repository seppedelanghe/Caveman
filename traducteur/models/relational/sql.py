import os
import json

from uuid import uuid4
from datetime import datetime
from pydantic import BaseModel
from typing import TypeVar, List, Type

from sqlalchemy.orm import declarative_base
from sqlalchemy import String, Column, DATETIME

from ..base import BaseDatabaseModel
from ...managers.sql import SQLModelManager

T = TypeVar('T')


class BaseSQLModel:
    """
        SQL config
    """
    __table_args__ = {'mysql_engine': 'InnoDB'}

    """
        Base columns
    """
    id = Column(String(32), primary_key=True)

    created_at = Column(DATETIME(), default=datetime.utcnow(), nullable=False)
    updated_at = Column(DATETIME(), default=datetime.utcnow(), nullable=False)
    deleted_at = Column(DATETIME(), default=None, nullable=True)

    """
        Methods
    """
    def save(self):
        if self.exists(self.id):
            self.updated_at = datetime.utcnow()
            return self.manager().update(self)
        else:
            self.id = uuid4().hex
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            return self.manager().insert(self)

    def delete(self):
        return self.manager().delete(self)

    def map_to(self, cls: Type[BaseModel]):
        return cls(**self.dict())

    def dict(self):
        return self.__dict__

    """
        Properties
    """
    @property
    def classname(self) -> str:
        return self.__class__.__name__

    """
        Class methods
    """
    @classmethod
    def map_from(cls, item: BaseDatabaseModel) -> 'BaseSQLModel':
        return cls.from_dict(item.dict())

    @classmethod
    def from_dict(cls, values: dict) -> 'BaseSQLModel':
        return cls(**values)

    @classmethod
    def from_json(cls, data: str) -> 'BaseSQLModel':
        return cls.from_dict(json.loads(data))

    @classmethod
    def get(cls, id: str) -> 'BaseSQLModel':
        return cls.manager().get(cls, id)

    @classmethod
    def all(cls, **kwargs) -> List['BaseSQLModel']:
        return cls.manager().all(cls, **kwargs)

    @classmethod
    def paginate(cls, page: int = 0, per_page: int = 30, *args, **kwargs) -> List['BaseSQLModel']:
        return cls.manager().paginate(cls, page, per_page, *args, **kwargs)

    @classmethod
    def exists(cls, id: str) -> bool:
        return cls.manager().exists(cls, id)

    @classmethod
    def manager(cls) -> SQLModelManager:
        return SQLModelManager[cls](os.environ.get('SQL_CONNECTION_STRING'), os.environ.get('SQL_CONNECTION_PARAMS', None))


SQLBase = declarative_base(cls=BaseSQLModel)
