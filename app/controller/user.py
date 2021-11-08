import re
from flask_restful import Resource, reqparse, abort, fields, marshal
from app.service.user_service import user_service
from app.helpers.message_helpers import exception_converter, rest_exception


class User(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(User, self).__init__()

    def patch(self, user_id):
        try:

            # set expected arguments
            self.parser.add_argument(
                "op",
                type=str,
                required=True,
                choices=("activate"),
                help="activate is the only supported operation",
            )
            self.parser.add_argument("activation_code", type=str, required=False)
            self.parser.add_argument("password", type=str, required=False)

            # get the request body
            body_data = self.parser.parse_args()

            # validate body
            if body_data["op"] == "activate" and not body_data["activation_code"]:
                abort(400, message="activation code is missing for the operation")
            
            if body_data["op"] == "activate" and not body_data["password"]:
                abort(400, message="password is missing for the operation")

            if(bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})',body_data["password"]))==False):
                abort(400, message="Please choose a stronger password with one digit, a special character and an upper and a lower case character")

            # Initiaze Service
            user = user_service()
            _, email = user.activate_user(user_id, body_data["activation_code"],body_data["password"])

            return {"username": email, "message": "User has been activated"}

        except Exception as e:
            rest_exception(e)
