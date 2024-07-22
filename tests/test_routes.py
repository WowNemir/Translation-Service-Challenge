from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app import app
from bson import ObjectId

client = TestClient(app)

mock_word_id_1 = str(ObjectId())
mock_word_id_2 = str(ObjectId())

mock_word_id_1 = str(ObjectId())
mock_word_id_2 = str(ObjectId())

mock_word_data = {
    "id": mock_word_id_1,
    "language": "en",
    "targetLanguage": "de",
    "word": "hello",
    "translation": "hallo",
    "translations": {
        "Noun": [
            {"translation": "hallo", "synonyms": ["hi"], "frequency": 10}
        ]
    },
    "definitions": {
        "Noun": [
            {"definition": "A greeting", "example": "Hello, world!", "synonyms": {"normal": ["hi", "hey"]}}
        ]
    },
    "examples": ["Hello, world!"]
}

mock_words_data = [
    mock_word_data,
    {
        "id": mock_word_id_2,
        "language": "en",
        "targetLanguage": "de",
        "word": "cat",
        "translation": "Katze",
        "translations": {
            "Noun": [
                {"translation": "Katze", "synonyms": ["cat"], "frequency": 1}
            ]
        },
        "definitions": {
            "Noun": [
                {"definition": "A small domesticated carnivorous mammal"}
            ]
        },
        "examples": ["A marbled cat"]
    }
]

@patch('translate_client.TranslateClient.translate')
def test_get_word_details_found(mock_translate):
    with patch('db.words_collection.find_one') as mock_find_one:
        mock_find_one.return_value = mock_word_data
        response = client.get("/word/hello?language=en&target_language=de")
    print(response.json())
    print(mock_word_data)
    assert response.status_code == 200
    assert response.json() == mock_word_data

@patch('db.words_collection.delete_one')
def test_delete_word_success(mock_delete):
    mock_delete.return_value.deleted_count = 1
    
    response = client.delete(f"/word/{mock_word_id_1}")
    assert response.status_code == 200
    assert response.json() == {"message": "Word deleted successfully"}

@patch('db.words_collection.delete_one')
def test_delete_word_not_found(mock_delete):
    mock_delete.return_value.deleted_count = 0
    
    response = client.delete(f"/word/{mock_word_id_1}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Word not found"}

@patch('db.words_collection.find')
def test_get_words_list(mock_find):
    mock_cursor = MagicMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_words_data

    mock_find.return_value = mock_cursor

    response = client.get("/words/?limit=10")
    
    assert response.status_code == 200
    assert response.json() == mock_words_data

@patch('db.words_collection.find')
def test_get_words_list_exclude_definitions(mock_find):
    mock_data_exclude_definitions = deepcopy(mock_words_data)
    for word in mock_data_exclude_definitions:
        word.pop('definitions')

    mock_cursor = MagicMock()
    mock_cursor.sort.return_value = mock_cursor
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_data_exclude_definitions

    mock_find.return_value = mock_cursor
    
    response = client.get("/words/?limit=10&include_definitions=false")
    
    assert response.status_code == 200
    assert response.json() == mock_data_exclude_definitions

if __name__ == "__main__":
    pytest.main()
