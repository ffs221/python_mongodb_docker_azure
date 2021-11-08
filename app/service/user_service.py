from app.helpers.exception import ApiException
from app.config import config
from app.service.azure_b2c_service import create_and_set_password
from datetime import datetime


from bson.objectid import ObjectId
from app.model.users_model import Users
from flask_restful import Resource
import hashlib


class user_service(Resource):
    def __init__(self):
        self.users = Users()

    def get_user_by_id(self, user_id):
        try:
            return self.users.collection.find_one({"_id": ObjectId(user_id)})
        except Exception as e:
            raise Exception(e)

    def is_user_email_exist(self, email):
        if self.users.collection.count_documents({"email": email}, limit=1) != 0:
            return True
        return False

    def create_user(self, display_name, email, phone_number, invited_by=None, session=None):
        payload = {
            "name": display_name,
            "email": email,
            "phonenumber": phone_number,
            "active": False,
            "created_on": datetime.now(),
            "invitedby": invited_by,
            "sub": None,
            "integation_config": {
                "linkedin": {"token": None, "expiry": {"date": None}},
                "google_calender": {"token": None, "expiry": {"date": None}},
                "facebook": {"token": None, "expiry": {"date": None}},
                "twitter": {"token": None, "expiry": {"date": None}},
            },
            "notification_config": None,
        }
        try:
            document = Users(payload)
            document.save(session=session)
            return document._id, document.email
        except Exception as e:
            raise Exception(e)

    def activate_user(self, user_id, activation_code, password):
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                raise ApiException(404, "user not found")

            document = Users(user)

            # crate hash code to compare the activation code
            hash_value = document.name + "|" + config.HASH_KEY
            user_activation_code = hashlib.sha256(
                hash_value.encode("utf-8")
            ).hexdigest()

            if activation_code == user_activation_code:
                # create b2c account
                if create_and_set_password(document.name, document.email, password):
                    # update user as activted.
                    document.update({"active": True})
                    return document._id, document.email
                else:
                    raise ApiException(
                        400,
                        data={
                            "message": "Actiation failed : Unable to set the password, please try again"
                        },
                    )
            else:
                raise ApiException(
                    400, data={"message": "Actiation failed : invalid activation code"}
                )

        except Exception as e:
            raise e
