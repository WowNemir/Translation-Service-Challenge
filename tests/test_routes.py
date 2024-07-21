import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app

client = TestClient(app)

mock_word_data = {
    "word": "hello",
    "language": "en",
    "targetLanguage": "de",
    "id": "fake_id"
}

mock_translations = [
    {"word_id": "fake_id", "translation": "hallo", "synonyms": ["hi"], "frequency": 10}
]

mock_definitions = [
    {"word_id": "fake_id", "definition": "A greeting", "example": "Hello, world!", "synonyms": {"normal": ["hi"], "informal": ["hey"]}}
]

@patch('translate_client.TranslateClient.translate')
def test_get_word_details_found(mock_translate):
    mock_translate.return_value = {
        "translations": mock_translations,
        "definitions": mock_definitions
    }
    
    response = client.get("/word/hello?language=en&target_language=de")
    assert response.status_code == 200
    assert response.json() == {
        "id": "fake_id",
        "word": "hello",
        "language": "en",
        "targetLanguage": "de",
        "translations": mock_translations,
        "definitions": mock_definitions
    }

@patch('translate_client.TranslateClient.translate')
def test_get_word_details_not_found(mock_translate):
    mock_translate.return_value = {
        "translations": mock_translations,
        "definitions": mock_definitions
    }
    
    response = client.get("/word/nonexistentword?language=en&target_language=de")
    assert response.status_code == 200
    assert response.json() == {
        "id": "fake_id",
        "word": "nonexistentword",
        "language": "en",
        "targetLanguage": "de",
        "translations": mock_translations,
        "definitions": mock_definitions
    }

@patch('translate_client.TranslateClient.translate')
def test_get_word_details_insert(mock_translate):
    mock_translate.return_value = {
        "translations": mock_translations,
        "definitions": mock_definitions
    }
    
    response = client.get("/word/newword?language=en&target_language=de")
    assert response.status_code == 200
    assert response.json() == {
        "id": "fake_id",
        "word": "newword",
        "language": "en",
        "targetLanguage": "de",
        "translations": mock_translations,
        "definitions": mock_definitions
    }

@patch('db.words_collection.delete_one')
def test_delete_word_success(mock_delete):
    mock_delete.return_value.deleted_count = 1
    
    response = client.delete("/word/fake_id")
    assert response.status_code == 200
    assert response.json() == {"message": "Word deleted successfully"}

@patch('db.words_collection.delete_one')
def test_delete_word_not_found(mock_delete):
    mock_delete.return_value.deleted_count = 0
    
    response = client.delete("/word/fake_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Word not found"}

if __name__ == "__main__":
    pytest.main()
