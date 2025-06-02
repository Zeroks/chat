import pytest
import requests
import random
import string
import pydantic
from requests import Session


def generate_random_user():
    random_name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(2, 15)))
    return { "name": random_name , "age": f'{random.randint(1,150)}'}

@pytest.fixture(scope="function")
def first_random_user():
    return generate_random_user()
@pytest.fixture(scope="function")
def second_random_user():
    return generate_random_user()

def test_create_fin_user(first_random_user):
    #тестю создание
    test_user = first_random_user
    response = requests.post("http://127.0.0.1:5000/users", json=test_user)
    assert response.status_code == 200
    response_data = response.json()
    assert "user_id" in response_data
    test_user_id = response_data.get("user_id")
    assert test_user_id is not None
    search = requests.get(f'http://127.0.0.1:5000/users?q={test_user.get("name")}')
    search_data = search.json()
    result = next((item for item in search_data if item["user_id"] == test_user_id), None)
    assert result.get("user_id") == test_user_id
    #тестю поиск
    test_find = requests.get(f'http://127.0.0.1:5000/users?q={test_user.get("name")}')
    assert test_find is not []

def test_post_get_edit_messages(first_random_user, second_random_user):
    #тестю пост нового сообщения
    sender = requests.post("http://127.0.0.1:5000/users", json=first_random_user)
    recipient = requests.post("http://127.0.0.1:5000/users", json=second_random_user)
    sender_id = sender.json().get("user_id")
    recipient_id = recipient.json().get("user_id")
    test_conversation_id = sorted([sender_id,recipient_id])
    test_conversation_id = f'{test_conversation_id[0]}_{test_conversation_id[1]}'
    making_random_message = ''.join(random.choices(string.ascii_lowercase, k=random.randint(2,15)))
    response_test_post_new_message = requests.post(f'http://127.0.0.1:5000/messages/{test_conversation_id}', json={"sender":sender_id, "text": making_random_message})
    test_message_id = response_test_post_new_message.text
    assert test_message_id is not None
    #тестю получение
    test_get_messeges = requests.get(f'http://127.0.0.1:5000/messages/{test_conversation_id}')
    data_get_messages = test_get_messeges.json()
    search_message = next((item for item in data_get_messages if item["message_id"] == test_message_id), None)
    assert search_message.get("text") == making_random_message
    #тестю редактирование сообщения
    test_edit = requests.patch(f'http://127.0.0.1:5000/messages/{test_conversation_id}/{test_message_id}', json= {"text": "edited"})
    test_get_messeges = requests.get(f'http://127.0.0.1:5000/messages/{test_conversation_id}')
    data_get_messages = test_get_messeges.json()
    search_message = next((item for item in data_get_messages if item["message_id"] == test_message_id), None)
    assert search_message.get("text") == "edited"













