import sqlalchemy

from db import db

from datetime import datetime


class UrlModel(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    original_url = db.Column(db.String(5000), nullable=False, unique=True)
    clicks = db.Column(db.Integer, default=0, nullable=False)
