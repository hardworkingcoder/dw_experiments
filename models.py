from app import db
import datetime
from geoalchemy2 import Geometry
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column
import sqlalchemy
from slugify import slugify


class User(db.Model):
    
    __tablename__ = "users"
    
    user_uuid = Column(UUID(as_uuid=True),
        server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True)
    permissions_group = db.Column(db.String, default='user') # user, staff, admin
    email = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    datadotworld_access_token = db.Column(db.String) 
    data = db.Column(postgresql.JSONB, nullable=True)

class Session(db.Model):
    
    __tablename__ = "sessions"
    
    session_uuid = Column(UUID(as_uuid=True),
        server_default=sqlalchemy.text("uuid_generate_v4()"), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_uuid = Column(UUID(as_uuid=True), db.ForeignKey("users.user_uuid"), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)