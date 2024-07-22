from dataclasses import dataclass
import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, AfterValidator, PlainSerializer, WithJsonSchema, ConfigDict, field_validator
from typing import Annotated, Any, Dict, List, Optional, Union

def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]

class MongoModel(BaseModel):
    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }

class Synonyms(BaseModel):
    normal: Optional[List[str]] = None
    informal: Optional[List[str]] = None

class Definition(BaseModel):
    definition: Optional[str] = None
    example: Optional[str] = None
    synonyms: Optional[Synonyms] = None

class Translation(BaseModel):
    translation: Optional[str] = None
    synonyms: Optional[List[str]] = None
    frequency: Optional[int] = None

class Word(MongoModel):
    id: PyObjectId = Field(alias="_id")
    language: str = None
    targetLanguage: str = None
    word: str = None
    translation: Optional[str] = None
    wordTranscription: Optional[str] = None
    translationTranscription: Optional[str] = None
    translations: Optional[Dict[str, List[Translation]]] = None
    definitions: Optional[Dict[str, List[Definition]]] = None
    examples: Optional[List[str]] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)
