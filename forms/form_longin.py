from utils import Form, StringField,validators, PasswordField, FlaskForm, SubmitField

class form_login(FlaskForm):
    usuario = StringField('usuario', [
        validators.DataRequired(),
        validators.Length(min=4, max=25, message='El usuario con mal formato')
    ])
    contrasenia = PasswordField('contrasenia', [
        validators.DataRequired(),
        validators.Length(min=4, max=25, message='La contrasenia con mal formato')
    ])
    boton = SubmitField('Ingresar')