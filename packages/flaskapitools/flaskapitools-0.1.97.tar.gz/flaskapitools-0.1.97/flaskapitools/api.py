from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from flask_cors import CORS
#from flask_rest_paginate import Pagination
import importlib
from flask_restplus import Api as ApiRestplus
#from flask import Blueprint
from jsonschema import FormatChecker

load_dotenv()
database = SQLAlchemy()
flask_bcrypt = Bcrypt()
config = {}

authorizations = {
    'Basic Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

class AuthClass:
    MODEL = None


class Api():
    AuthClass = None
    app = None
    db = None
    api = None
    flask_bcrypt = None
    app_config=None

    def __init__(self, name, app_config={}):
        #super(ApiRestplus, self).__init__()
        
        self.app = Flask(name, template_folder='templates')
        self.db = database
        self.flask_bcrypt = Bcrypt()
        self.app_config = app_config

        decorators  = []
        for decorator in getattr(app_config, "DECORATORS", []):
            arrmod = decorator.split(".")
            _func = arrmod[-1]
            arrmod.pop()
            mod = importlib.import_module(".".join(arrmod))
            decorators.append(getattr(mod, _func))

        self.api = ApiRestplus(self.app,
            ui=app_config.DOC_UI if getattr(app_config, "DOC_UI", None) != None else True,
            doc="/" if getattr(app_config, "DOC_UI", None) != None and getattr(app_config, "DOC_UI", None)  else False,
            specs=app_config.DOC_UI if getattr(app_config, "DOC_UI", None) != None else True,
            security='Basic Auth',
            authorizations=authorizations,
            title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
            version='1.0',
            description='a boilerplate for flask restplus web service',
            format_checker=FormatChecker(formats=["date"]),
            decorators=decorators
        )

        auth_model = getattr(app_config, "AUTH_MODEL", None)
        if auth_model != None:
            arrmod = auth_model.split(".")
            _class = arrmod[-1]
            arrmod.pop()
            mod = importlib.import_module(".".join(arrmod))
            AuthClass.MODEL = getattr(mod, _class)
            #print(AuthClass.MODEL)

        for mod in getattr(app_config, "ROUTES", []):
            #full_module_name = "app.controller." + mod["controller"]
            #print(full_module_name)
            mymodule = importlib.import_module(mod["module"])
            #print(mymodule)
            controller = getattr(mymodule, mod["controller"])
            self.api.add_namespace(controller.api,path=mod["path"])

    
    def create_app(self, config_name="dev"):
        self.app.config['Upload_folder'] = './static/'
        CORS(self.app, supports_credentials=True, 
            #origins=["http://localhost:3000", "https://www.micasaldm.mx","http://192.168.0.12:3000","https://tec.apoyoestudiantil.mx", "http://tec.apoyoestudiantil.mx" ]
        )
        config = self.app_config
        self.app.config.from_object(self.app_config)

        self.db.init_app(self.app)
        self.flask_bcrypt.init_app(self.app)

        @self.app.teardown_appcontext
        def shutdown_session(exception=None):
            self.db.session.close()

        database = self.db
        flask_bcrypt = self.flask_bcrypt

        return self.app
    
    def get_api_db(self):
        return self.db



"""
app = Flask(__name__, template_folder='templates')
db = SQLAlchemy()
flask_bcrypt = Bcrypt()
pagination = Pagination(app, db)
blueprint = Blueprint('api', __name__, url_prefix="")

CONTROLLERS = [
    {"controller":"chatbot", "path":"/chatbot"}
]


api = Api(blueprint,
    doc=False, specs=False,
    security='Bearer Auth',
    authorizations=AUTHORIZATIONS,
    title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
    version='1.0',
    description='a boilerplate for flask restplus web service',
    format_checker=FormatChecker(formats=["date"])
)


for mod in CONTROLLERS:
    full_module_name = "app.main.controller." + mod["controller"]
    print(full_module_name)
    mymodule = importlib.import_module(full_module_name)
    print(mymodule)
    api.add_namespace(mymodule.api,path= mod["path"])



def create_app(config_name):
    app.config['Upload_folder'] = './static/'
    CORS(app, supports_credentials=True, origins=["http://localhost:3000", "https://www.micasaldm.mx","http://192.168.0.12:3000","https://tec.apoyoestudiantil.mx", "http://tec.apoyoestudiantil.mx" ])
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    #session  = Session(app)
    #app.config["SESSION_SQLALCHEMY"] = db
    #session.app.session_interface.db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.close()

    return app
"""