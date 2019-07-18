import datetime

from peewee import *

DATABASE = SqliteDatabase('entries.db')


class Entry(Model):
    """Entry is our only model indicating the columns of our table."""
    title = CharField()
    timestamp = DateTimeField()
    time_spent = CharField()
    content = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = {'-timestamp',}


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()