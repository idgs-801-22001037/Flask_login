from utils import Blueprint, render_template, redirect, url_for
from forms import form_login
from dao import dao_login
from utils import login_user, current_user, login_required
from models import Usuario

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/', methods=['GET','POST']) 
def index_login():
    form = form_login()
    titulo = 'hola'
    if form.validate_on_submit():
        usuario = form.usuario.data
        contrasenia = form.contrasenia.data
        user = Usuario.query.filter_by(nombre=usuario).first()
        if dao_login(usuario=usuario, contra=contrasenia):
            login_user(user) 
            print(f"Usuario logueado1: {current_user.is_authenticated}") 
            return redirect('/pizza/')
        else:
            return redirect('/')
    return render_template('pages/login.html', titulo=titulo, form=form)