# -*- coding: utf-8 -*-
import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from geoalchemy2 import Geometry
from sqlalchemy import or_, and_, between
from sqlalchemy.orm import aliased

from birdseye import db


class CMDR(object):
    '''
    Created, Modified, Deleted, Replication.
    '''
    created = db.Column(
        db.DateTime(),
        default=datetime.utcnow,
        nullable=False
    )
    modified = db.Column(
        db.DateTime(),
        default=None,
        onupdate=datetime.utcnow
    )
    deleted = db.Column(
        db.DateTime(),
        default=None,
        onupdate=datetime.utcnow
    )


class User(CMDR, db.Model):
    '''
    Users, many are present in the database.
    '''
    user_id = db.Column(UUID, primary_key=True)
    credentials = db.Column(JSONB)  # password, email, whatever
    settings = db.Column(JSONB)  # app personal settings
    social = db.Column(JSONB)  # public stuff: nick name, social links, etc.

    def __init__(self):
        pass


class Session(CMDR, db.Model):
    '''
    Sessions
    '''
    session_id = db.Column(UUID, primary_key=True)
    expires = db.Column(
        db.DateTime(),
        default=datetime.utcnow,
        nullable=False
    )
    user_id = db.Column(UUID)
    tokens = db.Column(JSONB)  # Related tokens (i.e. FCM, bla ba)

    def __init__(self):
        pass


class Observation(CMDR, db.Model):
    '''
    An observation by a user.
    '''
    observation_id = db.Column(UUID, primary_key=True)
    user_id = db.Column(UUID)
    location = db.Column(Geometry('POINT'))

    def __init__(self, user_id, location):
        self.id = str(uuid.uuid1())
        self.user_id = user_id
        self.location = location

    def __repr__(self):
        return '<Observation %r>' % self.observation_id
