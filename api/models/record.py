from peewee import *
import datetime

from db import DATABASE

class Record(Model):
    name = CharField()
    year_pressed = CharField()
    catalog_number = CharField()
    album_art = CharField()
    notes = CharField()
    created_at = DateTimeField(default = datetime.datetime.now)
    class Meta:
        database = DATABASE