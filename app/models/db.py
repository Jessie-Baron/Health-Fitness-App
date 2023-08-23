from flask_mongoengine import MongoEngine
from mongoengine import *

db = connect(host="mongodb://localhost:27017/health_fitness_app")['health_fitness_app']
