import certifi
import pymongo
from .config import config

client = pymongo.MongoClient(config.MONGO_URI, tlsCAFile=certifi.where())
db = client[config.DATABASE_NAME]
