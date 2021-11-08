import os
from pymongo import MongoClient
import certifi

basedir = os.path.abspath(os.path.dirname(__file__))
env_name = os.getenv("BOILERPLATE_ENV") or "dev"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "key123Magic")
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    # configu for mongo db
    DEFAULT_COMPANY_ID = "60adf3269fd4922bac86975e"
    BLOCKED_EMAIL_DOMAINS = ["gmail"]
    MONGO_URI = ("mongodb+srv://test:test@cluster0.7qgna.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" + str(certifi.where()))
    # MONGO_URI = str(MONGO_URI_ENV) + str(certifi.where())

    DATABASE_NAME = os.getenv("DATABASE_NAME")

    # config for sent grid
    SENT_GRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    ACTIVATE_EMAIL_TEMPLATE = "d-43ea0bf4b28f46cc9b25188f992b6b3a"
    FROM_EMAIL = "connect@fathurursaid.dev"

    # config for azure
    AZURE_B2C_CLIENT_ID = os.getenv("AZURE_B2C_CLIENT_ID")
    AZURE_B2C_SECRET = os.getenv("AZURE_B2C_SECRET")
    AZURE_B2C_SCOPE = os.getenv("AZURE_B2C_SCOPE")
    AZURE_B2C_TENENT = os.getenv("AZURE_B2C_TENENT")

    HASH_KEY = os.getenv("HASH_KEY")


class TestingConfig(Config):
    DEBUG = True
    # config for mongo db
    DEFAULT_COMPANY_ID = "60adf3269fd4922bac86975e"
    BLOCKED_EMAIL_DOMAINS = ["gmail"]
    MONGO_URI = ("mongodb+srv://test:test@cluster0.7qgna.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" + str(certifi.where()))
    # MONGO_URI = (
    #     os.getenv("MONGO_URI")
    #     + str(certifi.where())
    # )
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    # config for sent grid
    SENT_GRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    ACTIVATE_EMAIL_TEMPLATE = "d-43ea0bf4b28f46cc9b25188f992b6b3a"
    FROM_EMAIL = "connect@fathurursaid.dev"

    # config for azure
    AZURE_B2C_CLIENT_ID = os.getenv("AZURE_B2C_CLIENT_ID")
    AZURE_B2C_SECRET = os.getenv("AZURE_B2C_SECRET")
    AZURE_B2C_SCOPE = os.getenv("AZURE_B2C_SCOPE")
    AZURE_B2C_TENENT = os.getenv("AZURE_B2C_TENENT")

    HASH_KEY = os.getenv("HASH_KEY")


class ProductionConfig(Config):
    DEBUG = True
    # configu for mongo db
    DEFAULT_COMPANY_ID = "60adf3269fd4922bac86975e"
    BLOCKED_EMAIL_DOMAINS = ["gmail"]
    MONGO_URI = ("mongodb+srv://test:test@cluster0.7qgna.mongodb.net/myFirstDatabase?retryWrites=true&w=majority" + str(certifi.where()))
    # MONGO_URI = (
    #     os.getenv("MONGO_URI")
    #     + str(certifi.where())
    # )
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    # config for sent grid
    SENT_GRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    ACTIVATE_EMAIL_TEMPLATE = "d-43ea0bf4b28f46cc9b25188f992b6b3a"
    FROM_EMAIL = "connect@fathurursaid.dev"

    # config for azure
    AZURE_B2C_CLIENT_ID = os.getenv("AZURE_B2C_CLIENT_ID")
    AZURE_B2C_SECRET = os.getenv("AZURE_B2C_SECRET")
    AZURE_B2C_SCOPE = os.getenv("AZURE_B2C_SCOPE")
    AZURE_B2C_TENENT = os.getenv("AZURE_B2C_TENENT")

    HASH_KEY = os.getenv("HASH_KEY")


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)
config = config_by_name[env_name]
key = Config.SECRET_KEY
