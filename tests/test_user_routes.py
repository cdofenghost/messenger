import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..main import app
from ..backend.logic.exceptions import *
from ..backend.logic.routes.users import UserCreateSchema
from ..backend.database import get_db

client = TestClient(app)
db: Session = get_db()

@pytest.mark.asyncio
@pytest.mark.parametrize("creation_schema, expected_status_code, expected_message", [
    ### Positive cases
    (
        UserCreateSchema(email="d@gmail.com", password='123123123', repeated_password='123123123'),
        201,
        None,
    ), # Create First User

    ### Negative cases
    (
        UserCreateSchema(email="b@gmail.com", password='123123123', repeated_password='000000000'),
        400,
        "Password doesn't match the repeated password. Try again.",
    ), # Repeated password doesn't match the OG one
    (
        UserCreateSchema(email="d@gmail.com", password='123123123', repeated_password='123123123'),
        400,
        "Such e-mail has already been registered.",
    ), # User already registered (email already exists)
    (
        UserCreateSchema(email="a@owkfoaro.c", password='123123123', repeated_password='123123123'),
        400,
        "E-mail that you've given is inactive/unreachable/doesn't exist.",
    ), # Unreachable/non-existing email
])
async def test_register(creation_schema: UserCreateSchema,
                        expected_status_code: int,
                        expected_message: str):
    # Act
    response = client.post(url='/users/register', content=creation_schema.model_dump_json())

    # Assert
    assert response.status_code == expected_status_code
    if response.status_code >= 400:
        assert response.json()['detail'] == expected_message