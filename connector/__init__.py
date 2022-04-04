from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)
app.config.from_object('config')

from connector.controllers import routes