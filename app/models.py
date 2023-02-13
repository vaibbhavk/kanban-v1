from app.database import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.now())


class List(db.Model):
    __tablename__ = 'lists'
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    cards = db.relationship(
        "Card",
        cascade="all, delete",
        back_populates="list_ref")

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.now())


class Card(db.Model):
    __tablename__ = 'cards'
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    deadline = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Integer, nullable=False, default=False)
    completed_datetime = db.Column(db.DateTime(timezone=True))
    list = db.Column(db.Integer, db.ForeignKey(
        'lists.list_id', ondelete="CASCADE"), nullable=False)
    list_ref = db.relationship(
        "List",
        back_populates="cards")
        
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.now())