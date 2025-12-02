from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Projecte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titol = db.Column(db.String(150), nullable=False)
    descripcio = db.Column(db.Text, nullable=True)
    objectiu = db.Column(db.Float, nullable=False, default=100.0)
    recaptat = db.Column(db.Float, nullable=False, default=0.0)
    data_inici = db.Column(db.DateTime, default=datetime.utcnow)
    data_limit = db.Column(db.Date, nullable=True)
    minim_per_donacio = db.Column(db.Float, default=1.0)   # mínim per transacció
    maxim_per_donant = db.Column(db.Float, default=50.0)   # màxim acumulat per donant
    maxim_projecte = db.Column(db.Float, default=200.0)    # màxim total del projecte

class Aportacio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projecte_id = db.Column(db.Integer, db.ForeignKey('projecte.id'), nullable=False)
    usuari = db.Column(db.String(100), nullable=False)
    quantitat = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    projecte = db.relationship('Projecte', backref=db.backref('aportacions', lazy=True))
