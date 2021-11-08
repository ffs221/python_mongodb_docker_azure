from app.controller.user import User
from flask_restful import Resource, reqparse, abort, fields, marshal
from app.service.user_service import user_service
from app.service.company_service import company_service
from app.service.sendgrid_service import sent_activation_email
from app.helpers.message_helpers import format_exception, rest_exception
from app.helpers.validate_helpers import isEmailValid
from app.config import config
from app.database import client
import hashlib

company_fields = {
    "username": fields.String(attribute="email"),
    "companyname": fields.String(attribute="company_name"),
}


class Company(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        super(Company, self).__init__()

    def post(self):
        try:
            self.parser.add_argument(
                "display_name", type=str, required=True, help="Name can not be blank"
            )
            self.parser.add_argument(
                "company_name",
                type=str,
                required=True,
                help="Company name  can not be blank",
            )
            self.parser.add_argument(
                "company_type",
                type=str,
                required=True,
                choices=("agency", "company"),
                help="possible choice is agency or company",
            )
            self.parser.add_argument(
                "email", type=str, required=True, help="Email can not be blank"
            )
            self.parser.add_argument(
                "phone_number",
                type=str,
                help="Phone Number of the of the user registring",
            )

            body_data = self.parser.parse_args()

            # Validation of email
            email = body_data["email"]

            if not isEmailValid(email):
                abort(
                    422,
                    message="Please use your company email address, public email address are not allowed.",
                )

            # Validation of identity and company
            user = user_service()
            if user.is_user_email_exist(email):
                abort(
                    422,
                    message="The email you provided is already registred, please signin.",
                )

            company = company_service()
            if company.exists(
                {
                    "$or": [
                        {"name": body_data["company_name"]},
                        {"phone_number": body_data["phone_number"]},
                    ]
                }
            ):
                abort(422, message="This company name/phone number already registred.")

            with client.start_session() as session:

                def register_company_with_admin_user(session):
                    user_id, _ = user.create_user(
                        body_data["display_name"],
                        body_data["email"],
                        body_data["phone_number"],
                        session=session,
                    )
                    body_data["user_id"] = user_id
                    _, _ = company.create_company(body_data, session=session)

                session.with_transaction(register_company_with_admin_user)

            # crate hash code for acticvation email
            hash_value = body_data["display_name"] + "|" + config.HASH_KEY
            user_activation_code = hashlib.sha256(
                hash_value.encode("utf-8")
            ).hexdigest()
            sent_activation_email(
                body_data["email"],
                body_data["display_name"],
                str(body_data["user_id"]),
                user_activation_code,
            )

            return marshal(body_data, company_fields), 200

        except Exception as e:
            rest_exception(e)
