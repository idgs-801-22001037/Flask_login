
from routes import login_bp, pizza_bp
from utils import db, Flask, CSRFProtect, LoginManager, UserMixin, login_required, logout_user, redirect, session,url_for, current_user
from config import Config
from models import Usuario
from datetime import timedelta
import os


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(login_bp)
app.register_blueprint(pizza_bp)
#app.permanent_session_lifetime = timedelta(seconds=10)
app.config['SECRET_KEY'] = 'clave_secreta_segura'

csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login.index_login"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))  # Flask-Login necesita esta función


@app.route('/salir')
def salir():
    logout_user()
    print(f"Usuario logueado al salir: {current_user.is_authenticated}")
    return redirect('/')




if __name__ == '__main__':
    db.init_app(app=app)
    with app.app_context():
        db.create_all()
    csrf.init_app(app=app)
    app.run(debug=True, port=8080)