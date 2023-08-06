import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from .api import database as db
import importlib
from dotenv import load_dotenv
load_dotenv()

application = None
migrate = None

class ApiManager():
    def __init__(self, app):
        application = app
        application.app_context().push()
        manager = Manager(application)

        migrate = Migrate(application, db, directory="./database/"+os.getenv('ENV')+"/migrations/")
        manager.add_command('db', MigrateCommand)

        with application.app_context():
            from .models import imports

        with application.app_context():
            """"""
            arr = os.listdir('app/models')
            for f in arr:
                if ".py" in f:
                    full_module_name = "app.models."+f[0:-3]
                    #print(full_module_name)
                    mymodule = importlib.import_module(full_module_name)
                    #print(mymodule)

        @manager.command
        def start():
            application.run(host="0.0.0.0")
        
        manager.run()