import unittest
from unittest.mock import patch
from mongomock import MongoClient
import app.database
from app.service.user_service import user_service


class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.client = patch.object(app.database, "client", PyMongoMock())

    def test_create_user(self):
        user = user_service()
        body_data = {
            "display_name": "test",
            "email": "testemail@nyu.com",
            "phone_number": "0585640363",
        }
        _id, email = user.create_user(
            body_data["display_name"],
            body_data["email"],
            body_data["phone_number"],
            session=None,
        )
        self.assertEqual(email, "testemail@nyu.com")

    def test_is_user_email_exist(self):
        user = user_service()
        response = user.is_user_email_exist("testemail@nyu.com")
        self.assertTrue(response)

    # def drop_user_collection(self):
    #     db["Users"].drop()
