import datetime
from bson import ObjectId
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field, PrivateAttr, root_validator, validator
from typing import Dict, List, Optional
import pymongo
from translate import run_and_parse_js
app = FastAPI()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["word_database"]
collection = db["words"]

class MongoModel(BaseModel):
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
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
    id: Optional[str] = Field(alias="_id")
    language: str = 'en'
    targetLanguage: str = 'de'
    word: Optional[str] = None
    translation: Optional[str] = None
    wordTranscription: Optional[str] = None
    translationTranscription: Optional[str] = None
    translations: Optional[Dict[str, List[Translation]]] = None
    definitions: Optional[Dict[str, List[Definition]]] = None
    examples: Optional[List[str]] = None
    
    @root_validator(pre=True)
    def convert_empty_lists_to_dicts(cls, values):
        # Convert empty lists to empty dictionaries for 'translations' and 'definitions' fields
        if 'translations' in values and values['translations'] == []:
            values['translations'] = {}
        if 'definitions' in values and values['definitions'] == []:
            values['definitions'] = {}
        return values

    @classmethod
    def model_validate(cls, item: dict):
        try:
            # Create an instance of Word with defaults applied to missing fields
            word_obj = cls(**item)

            # Convert to dictionary and return
            return word_obj.dict()
        except Exception as e:
            return {}

@app.get("/word/{word}")
async def get_word_details(word: str, language: str = 'en', target_language = 'de', include_definitions: bool = False,
                           include_synonyms: bool = False, include_translations: bool = False):
    word_data = collection.find_one({"word": word})
    if word_data:
        return Word(**word_data)
    data_from_google = run_and_parse_js(word, language, target_language)
    data_from_google['language'] = language
    data_from_google['targetLanguage'] = target_language
    new_word = Word(**data_from_google)

    # print(type(new_word.dict()))
    collection.insert_one(new_word.model_dump())
    
    return new_word

@app.get("/words/")
async def get_words_list(skip: int = 0, limit: int = 10, sort_by: str = "word",
                         filter_word: Optional[str] = None):
    query = {}
    if filter_word:
        query["word"] = {"$regex": filter_word, "$options": "i"}
    
    words = collection.find(query).sort(sort_by).skip(skip).limit(limit)
    return list(map(Word.model_validate, words))

@app.delete("/word/{word_id}")
async def delete_word(word_id: str):
    result = collection.delete_one({"_id": word_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Word not found")
    return {"message": "Word deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
