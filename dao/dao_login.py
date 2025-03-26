from models import Usuario
from utils import db, abort, session, login_user
from datetime import datetime

def dao_login(usuario, contra):
    usuario_obj = db.session.query(Usuario).filter_by(nombre=usuario, contrasenia=contra).one_or_none()
    if usuario_obj is None:
        return False
    user = Usuario.query.filter_by(nombre=usuario).first()
    login_user(user, remember=True)  
    return True