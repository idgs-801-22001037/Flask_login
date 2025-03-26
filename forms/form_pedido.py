from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, IntegerField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired 
from wtforms import BooleanField  

class form_pedido(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    tamanio = RadioField('Tamaño', choices=[('chica', 'Chica -> $40'), ('mediana', 'Mediana -> $80'), ('grande', 'Grande -> $120')], validators=[DataRequired()])
    # Usamos BooleanField para cada ingrediente
    jamon = BooleanField('Jamón -> $10')
    pina = BooleanField('Piña -> $10')
    champi = BooleanField('Champiñón -> $10')
    num_pizza = IntegerField('Número de Pizzas', validators=[DataRequired()])
    submit = SubmitField('Agregar')
