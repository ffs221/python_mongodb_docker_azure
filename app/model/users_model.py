from .mongodB_model import Model
from app.database import db


class Users(Model):
    collection = db["Users"]

    @property
    def keywords(self):
        return self.title.split()
