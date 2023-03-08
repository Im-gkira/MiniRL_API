from marshmallow import fields, Schema
from datetime import datetime


class UrlSchema(Schema):
    id = fields.Integer(dump_only=True)
    created = fields.DateTime(dump_only=True, default=datetime.utcnow)
    original_url = fields.String(required=True)
    clicks = fields.Integer(dump_only=True, default=0)
