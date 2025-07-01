import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from models.models import ChatAPIClient, UserDTO, Message

def pytest_addoption(parser):
    parser.addoption(
        "--host",
        action="store",
        default="http://127.0.0.1:5000"
    )


@pytest.fixture
def host(request):
    host = request.config.getoption("--host")
    return ChatAPIClient(host=host)

@pytest.fixture
def test_user(request):
    return UserDTO(name = "vasya", age = 23, hobby = ["chess","soccer"])

@pytest.fixture
def test_message(request):
    return Message(sender="vovchik", text="privet,vasya")

@pytest.fixture
def conversation_id(request):
    return "vovchik_test"