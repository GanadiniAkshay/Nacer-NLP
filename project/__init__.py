import os
import time
import spacy


from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.components import ComponentBuilder

from werkzeug.contrib.cache import SimpleCache
from duckling import Duckling

from project.config import DevelopmentConfig

# instantiate the db
db = SQLAlchemy()
# instantiate flask migrate
migrate = Migrate()
# instantiate a cache
cache = SimpleCache()
#set up spacy nlp
nlp = spacy.load('en')
# set up duckling
d = Duckling()
d.load()


interpreters = {}


#set up the trainer
print("Setting up trainer")
config = os.path.join(os.getcwd(),'project', 'config.json')
builder = ComponentBuilder(use_cache=True) 
trainer = Trainer(RasaNLUConfig(config),builder)


def create_app():

    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from project.api.users import users_blueprint
    from project.api.bots  import bots_blueprint
    from project.api.nlu   import nlu_blueprint
    from project.api.intents import intents_blueprint
    from project.api.entities import entities_blueprint
    
    app.register_blueprint(users_blueprint)
    app.register_blueprint(bots_blueprint)
    app.register_blueprint(nlu_blueprint)
    app.register_blueprint(intents_blueprint)
    app.register_blueprint(entities_blueprint)

    # register default route
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        return render_template('index.html',cdn=DevelopmentConfig.CDN_URL)

    time1 = time.time()
    print("creating interpreters")
    create_interpreters(db)
    time2 = time.time()
    print(time2-time1)

    return app

def create_interpreters(db):
    from project.helpers.parser import NLUParser
    if os.path.exists('./models'):
        directories =os.listdir('./models')
        config = './project/config.json'
        for directory in directories:
            active_model = 'models/' + directory
            print(active_model)
            interpreters[active_model] = NLUParser(active_model,config, builder)