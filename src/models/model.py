from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, DateTime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


db = SQLAlchemy()

class Banned(db.Model):
    __tablename__ = 'banned'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(String(150), nullable=False)
    app_uuid = db.Column(String(150), nullable=False)
    blocked_reason = db.Column(String(255), nullable=False)
    created_at = db.Column(DateTime, nullable=False)
