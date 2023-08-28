from mongoengine import *

class Runs(EmbeddedDocument):
    run_id = SequenceField()
    date = StringField()
    duration = StringField()
    distance = FloatField()