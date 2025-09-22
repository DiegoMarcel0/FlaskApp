from flask import Flask, request
from models.helloMySQL import db
from dbconfig import Config
from views.helloMySQL_view import empleado_bp

#db = SQLAlchemy(app)
app = Flask(__name__)


app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(empleado_bp, url_prefix ="/empleado")

@app.route('/')
def main():
    return "Hola Mundo :v"
    #return redirect(url_for('datos'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True, port=4999)


#url_for usa los nombres de las funciones