from datetime import datetime
from pydantic import Field
from typing import Optional
import os

from traducteur.lib.model import BaseModel
from traducteur.lib.manager import MongoModelManager


class BaseSQLiteModel(BaseModel):
    id: str

    @property
    def _manager(self):
        return self.__class__.__get_manager()

    @property
    def _col_name(self):
        return self.__class__.__name__

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
    
    def save(self):
        if self.created_at == None:
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            return self._manager.insert_one(self)
        else:
            self.updated_at = datetime.utcnow()
            return self._manager.update_one(self)

    def delete(self):
        self.deleted_at = datetime.utcnow()
        return self._manager.delete_one(self)

    @classmethod
    def __get_manager(cls):
        con_str = os.environ['TRADUCTEUR_CONNECTION_STR']
        db_name = os.environ['TRADUCTEUR_CONNECTION_STR']
        return MongoModelManager(con_str, db_name)

    @classmethod
    def get(cls, id: str):
        manager = cls.__get_manager()
        result = manager.get_one(cls.__name__, id)
        return cls.from_dict(result)

    @classmethod
    def from_dict(cls, values: dict):
        return cls(**values)