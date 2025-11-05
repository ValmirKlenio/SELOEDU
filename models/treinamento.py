from extensions import db
from datetime import datetime

class Treinamento(db.Model):
    __tablename__ = 'treinamentos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    data_inicio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime)
    coordenador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    coordenador = db.relationship('User', backref=db.backref('treinamentos', lazy=True))

    def __repr__(self):
        return f'<Treinamento {self.nome}>'
