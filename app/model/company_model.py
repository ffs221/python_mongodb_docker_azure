import os, sys
from .mongodB_model import Model

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from app.database import db


class Company(Model):
    collection = db["Company"]

    @property
    def keywords(self):
        return self.title.split()
