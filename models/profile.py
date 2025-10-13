from extensions import db

class Profile(db.Model):
    __tablename__ = "profile"

    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    telefone       = db.Column(db.String(11), nullable=True)
    instituicao    = db.Column(db.String(100), nullable=True)
    cargo          = db.Column(db.String(50), nullable=True)
    bio            = db.Column(db.String(1000), nullable=True)
    foto           = db.Column(db.String(4))
    foto_thumb     = db.Column(db.String(300))

    user = db.relationship('User', back_populates='profile')