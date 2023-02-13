from flask import Flask
from app.database import db
from flask_login import LoginManager
from app.models import User
from app.config import LocalDevelopmentConfig
from flask_restful import  Api

app = Flask(__name__, template_folder="templates")

app.config.from_object(LocalDevelopmentConfig)

db.init_app(app)

api = Api(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

app.app_context().push()



# Import all the controllers so they are loaded
from app.controllers import *

# Import all the api controllers so they are loaded
from app.api import ListAPI, CardAPI
api.add_resource(ListAPI, '/api/list', '/api/list/<int:id>')
api.add_resource(CardAPI, '/api/card', '/api/card/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
