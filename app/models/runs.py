from mongoengine import *

class Runs(EmbeddedDocument):
    run_id = SequenceField()
    date = DateTimeField()
    duration = StringField()
    distance = FloatField()