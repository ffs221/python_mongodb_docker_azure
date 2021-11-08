from datetime import timedelta
from bson.objectid import ObjectId
from flask_restful import Resource
from datetime import datetime
from app.model.company_model import Company
from app.config import config


class company_service(Resource):
    def __init__(self):
        self.company = Company()

    def exists(self, query):
        if self.company.collection.count_documents(query, limit=1) != 0:
            return True
        return False

    def create_company(self, data, session=None):

        # copy the default company
        payload = self.company.collection.find_one(
            {"_id": ObjectId(config.DEFAULT_COMPANY_ID)}
        )

        # remove the _id key to force creat
        del payload["_id"]

        # set values
        payload["name"] = data["company_name"]
        payload["phone"] = data["phone_number"]
        payload["companytype"] = data["company_type"]
        payload["created_by"] = data["user_id"]

        payload["teams"][0]["members"][0] = payload["users"][0]["user_id"] = data[
            "user_id"
        ]
        payload["departments"][0]["createdby"] = data["user_id"]

        # set the trail period to 14 days from today.
        subscription_end_date = datetime.today() + timedelta(days=14)
        payload["suscription"][0]["subscription_start"] = datetime.today()
        payload["suscription"][0]["suscription_end"] = subscription_end_date

        # set the next payment to subscription end date
        payload["recurring_payment"]["next_payment_date"] = subscription_end_date

        try:
            document = Company(payload)
            document.save(session=session)
            return document._id, document.name
        except Exception as e:
            raise Exception(e)
