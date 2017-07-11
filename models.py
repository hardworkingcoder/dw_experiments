from app import db
import datetime
from geoalchemy2 import Geometry
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column
import sqlalchemy
from slugify import slugify
from flask.ext.login import UserMixin

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True),
        server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True)
    session_token = Column(UUID(as_uuid=True),
        server_default=sqlalchemy.text("uuid_generate_v4()"), unique=True)
    permissions_group = db.Column(db.String, default='user') # user, staff, admin
    ddw_access_token = db.Column(db.String)
    ddw_token_expires_in = db.Column(db.Integer)
    ddw_avatar_url = db.Column(db.String)
    nickname = db.Column(db.String)
    social_id = db.Column(db.String, unique=True)
    ddw_user_created = db.Column(db.Date)
    ddw_user_updated = db.Column(db.Date)
    data = db.Column(postgresql.JSONB, nullable=True)

    def get_id(self):
        return unicode(self.session_token)