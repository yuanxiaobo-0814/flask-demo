
from flask_sqlalchemy import sqlalchemy
from . import db


class User(db.Model):
    """用户基础表"""
    __tablename__ = 't_user'
    __table_args__ = (
        {'comment': '用户基础表'}
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, index=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(200))
    nickname = db.Column(db.String(100))
    department = db.Column(db.String(50))
    avatar = db.Column(db.String(256))
    phone = db.Column(db.String(11))
    status = db.Column(db.String(32))
    last_login_ip = db.Column(db.String(20))
    last_login_time = db.Column(db.DATETIME())
    created_time = db.Column(
        db.DATETIME(), server_default=sqlalchemy.sql.func.now())
    updated_time = db.Column(db.DATETIME(), server_default=sqlalchemy.text(
        'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
