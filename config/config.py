# esto modulo crea una clase con la configuracion para conectarce a una BD mysql
class Config():
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/pizzeria'
    SQLALCHEMY_TRACK_MODIFICATIONS = False