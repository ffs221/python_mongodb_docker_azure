import flask
import flask_restful as restful
from .config import config_by_name
import sys

sys.stdout.flush()

app = flask.Flask(__name__)


def create_app(config_name):
    app.config.from_object(config_by_name[config_name])
    api = restful.Api(app)

    # add resource section starts here ----
    from .controller.company import Company
    from .controller.user import User

    api.add_resource(Company, "/api/v1/companies")
    api.add_resource(User, "/api/v1/user/<user_id>")

    return app
