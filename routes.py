from typing import Optional
from fastapi import APIRouter, HTTPException
from models import Word, Translation, Definition
from db import words_collection
from translate_client import TranslateClient
from bson import ObjectId

router = APIRouter()


@router.get("/word/{word}")
async def get_word_details(word: str, language: str = 'en', target_language='de'):
    word_data = words_collection.find_one({"word": word})
    if word_data:
        return Word(**word_data)
    data_from_google = TranslateClient().translate(word, language, target_language)
    data_from_google['language'] = language
    data_from_google['targetLanguage'] = target_language

    res = words_collection.insert_one(data_from_google)
    data_from_google['id'] = res
    return Word(**data_from_google)

@router.get("/words/")
async def get_words_list(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "word",
    filter_word: Optional[str] = None,
    include_definitions: bool = False,
    include_synonyms: bool = False,
    include_translations: bool = False,
    include_examples: bool = False
):
    query = {}
    if filter_word:
        query["word"] = {"$regex": filter_word, "$options": "i"}

    projection = {}
    if not include_definitions:
        projection['definitions'] = 0
    if not include_synonyms:
        projection['synonyms'] = 0
    if not include_translations:
        projection['translations'] = 0
        projection['translation'] = 0
        projection['wordTranscription'] = 0
        projection['translationTranscription'] = 0
        projection['language'] = 0
        projection['targetLanguage'] = 0
    if not include_examples:
        projection['examples'] = 0

    words_cursor = words_collection.find(query, projection=projection).sort(sort_by).skip(skip).limit(limit)
    results = [Word(**word_data) for word_data in words_cursor]

    return [model.model_dump(exclude_defaults=True) for model in results]

@router.delete("/word/{word_id}")
async def delete_word(word_id: str):
    result = words_collection.delete_one({"_id": ObjectId(word_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Word not found")
    return {"message": "Word deleted successfully"}
