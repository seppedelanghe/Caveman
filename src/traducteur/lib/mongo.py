from pydantic import Field
from typing import Optional
from bson import ObjectId
import os, logging

from traducteur.lib.model import BaseModel
from traducteur.lib.manager import MongoModelManager

class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class BaseMongoModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias='_id')

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str,
            PydanticObjectId: str
        }

    @classmethod
    def __get_manager(cls):
        con_str = os.environ['TRADUCTEUR_CONNECTION_STR']
        db_name = os.environ['TRADUCTEUR_DATABASE']
        return MongoModelManager(con_str, db_name)

    