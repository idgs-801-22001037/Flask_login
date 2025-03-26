from utils import db
from datetime import datetime
from sqlalchemy.sql import func

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, server_default=func.now())
    total = db.Column(db.Float, nullable=False)  # Total de la venta
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), nullable=False)  # Persona (cliente)

    # Relación con la persona (cliente)
    persona = db.relationship('Persona', backref=db.backref('ventas', lazy=True))

    # Relación con las pizzas
    #cpizzas = db.relationship('Pizza', backref='venta', lazy=True)
