import requests
import pydantic
import pytest
from pydantic import BaseModel
from requests import Session

class UserDTO(BaseModel):
    name: str
    age: int
    hobby: list

class Message(BaseModel):
    sender: str
    text: str

class ChatAPIClient:
    def __init__(self, host="http://127.0.0.1:5000"):
        self.session = Session()
        self.host = host

    def create_user(self, user: UserDTO)->str:
        response = self.session.post(f"{self.host}/users", json=user.model_dump())
        response.raise_for_status()
        return response.json()["user_id"]

    def find_user(self, name: str )->list:
        response = self.session.get(f"{self.host}/users?q={name}")
        response.raise_for_status()
        return response.json()

    def post_message(self,conversation_id: str , message: Message)->str:
        response = self.session.post(f"{self.host}/messages/{conversation_id}", json=message.model_dump())
        response.raise_for_status()
        return response.json().get("message_id")

    def get_messages(self, conversation_id: str)->list:
        response = self.session.get(f"{self.host}/messages/{conversation_id}")
        response.raise_for_status()
        return response.json()

    def edit_message(self, conversation_id: str, message_id: str, new_text: str)->None:
        response = self.session.patch(f"{self.host}/messages/{conversation_id}/{message_id}", json={"text": new_text})
        response.raise_for_status()


