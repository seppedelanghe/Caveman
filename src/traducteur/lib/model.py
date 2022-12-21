from pydantic import BaseModel as BasePydanticModel
from datetime import datetime
from typing import Optional, Any
import logging, os

from .manager import BaseModelManager

class BaseModel(BasePydanticModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    '''
        Properties
    '''
    @property
    def column_names(self):
        return [str(col).lower() for col in self.dict().keys()]

    @property
    def column_values(self):
        return tuple([str(v) for v in self.dict().values()])

    @property
    def _manager(self) -> BaseModelManager:
        return self.__class__.__get_manager()

    @property
    def _col_name(self):
        return self.__class__.__name__


    '''
        Init
    '''
    def __init__(__pydantic_self__, **data: Any):
        super().__init__(**data)


    '''
        Crud
    '''
    def save(self):
        if self.created_at == None:
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            self.id = self._manager.insert_one(self)
        else:
            self.updated_at = datetime.utcnow()
            self._manager.update_one(self)

        return self

    def delete(self):
        self.deleted_at = datetime.utcnow()
        return self._manager.delete_one(self)


    '''
        Classmethods
    '''
    @classmethod
    def get(cls, id: str):
        pass

    @classmethod
    def get_where(cls, query):
        pass

    @classmethod
    def exists(cls, id):
        pass

    @classmethod
    def exists_where(cls, query):
        pass

    @classmethod
    def __get_manager(cls) -> BaseModelManager:
        pass

    @classmethod
    def from_dict(cls, values: dict):
        return cls(**values)



class BaseSQLModel(BaseModel):
    @classmethod
    def get(cls, id: str):
        manager = cls.__get_manager()
        result = manager.get_one(cls.__name__, id)
        return cls.from_dict(result) if result else None

    @classmethod
    def get_where_raw(cls, query, **kwargs):
        manager = cls.__get_manager()
        return manager.get_many(cls.__name__, query, **kwargs)

    @classmethod
    def get_where(cls, query, **kwargs):
        result = cls.get_where_raw(query, **kwargs)
        return [cls.from_dict(i) for i in result] if len(result) > 0 else None

    @classmethod
    def get_one_where(cls, query, **kwargs):
        manager = cls.__get_manager()
        result = manager.get_one(cls.__name__, query, **kwargs)
        return cls.from_dict(result) if result else None

    @classmethod
    def all(cls, **kwargs):
        manager = cls.__get_manager()
        result = manager.get_all(cls.__name__, **kwargs)
        return [cls.from_dict(i) for i in result] if len(result) > 0 else None

    @classmethod
    def exists(cls, id: str) -> bool:
        try:
            return cls.__get_manager().exists(cls.__name__, id=id)
        except Exception:
            return False

    @classmethod
    def exists_where(cls, query) -> bool:
        try:
            return cls.__get_manager().exists_where(cls.__name__, query)
        except Exception as e:
            return False


    @property
    def sql_columns(self):
        return ', '.join(self.column_names)

    @property
    def sql_values(self):
        return ', '.join(self.column_values)

    @property
    def q_marks(self):
        return ', '.join(['?' for _ in range(len(self.column_names))])

    @property
    def sql_update(self):
        return ', '.join([f"{str(col).lower()} = {val}" for col, val in self.dict().items()])