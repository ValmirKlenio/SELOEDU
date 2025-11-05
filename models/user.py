from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id             = db.Column(db.Integer, primary_key=True)
    nome           = db.Column(db.String(100), nullable=False)
    email          = db.Column(db.String(150), unique=True,nullable=False)
    password_hash  = db.Column(db.String(200), nullable=False)
    role           = db.Column(db.String(20), nullable=False, default = 'master')
    ativo          = db.Column(db.Boolean, default=True)


    profile = db.relationship('Profile', uselist=False, back_populates='user', cascade="all, delete")


    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)