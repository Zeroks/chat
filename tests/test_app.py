import pytest
import requests
import random
import string
import pydantic
import conftest
from pydantic import BaseModel
from requests import Session

def test_create_user(host, test_user):
    user_id = host.create_user(test_user)
    assert isinstance(user_id, str)
    assert len(user_id) > 0

def test_find_user(host,test_user):
    user_id = host.create_user(test_user)
    search_result = host.find_user(test_user.name)
    assert isinstance(search_result, list)
    assert search_result[0].get("name") == test_user.name

def test_movement_with_messages(host, conversation_id, test_message):
    #тестю отправку сообщения
    message_id = host.post_message(conversation_id, test_message)
    assert isinstance(message_id, str)
    assert len(message_id) > 0
    #тестю получение сообщений
    get_result = host.get_messages(conversation_id)
    assert isinstance(get_result, list)
    assert get_result[0].get("text") == test_message.text
    #тестю редактирование сообщений
    new_text = "poka,vasya"
    host.edit_message(conversation_id, message_id, new_text)
    updated_messages = host.get_messages(conversation_id)
    assert updated_messages[0].get("text") == new_text




















