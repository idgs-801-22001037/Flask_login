from utils import db

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tamanio = db.Column(db.String(50), nullable=False)
    ingredientes = db.Column(db.String(150), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)  # Relación con la venta

    # Relación con Venta
    venta = db.relationship('Venta', backref=db.backref('pizzas', lazy=True))
