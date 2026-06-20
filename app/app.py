from flask import Flask, render_template, send_from_directory#, request, redirect
from extensions import db
from dbconfig import Config
from views.helloMySQL_view import empleado_bp
from views.treasureLand_view import treasureLand_bp
from views.lewisStruct_view import lewis_bp
#db = SQLAlchemy(app)
app = Flask(__name__)
routes = {
    'empleado_bp':'/empleado',
    'treasureLand_bp':'/grafos',
    'lewis_bp':'/lewis'
}
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(empleado_bp, url_prefix =routes['empleado_bp'])
app.register_blueprint(treasureLand_bp, url_prefix =routes['treasureLand_bp'])
app.register_blueprint(lewis_bp, url_prefix =routes['lewis_bp'])

@app.route('/')
def main():
    index_routes = dict(zip(app.blueprints.keys(), routes.values()))
    return render_template("index.html", index_routes=index_routes)
    #return "Hola Mundo :v"
    #return redirect("/empleado")
#FAVICON
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        app.static_folder,
        'favicon.svg',
        mimetype='image/svg+xml'
        )
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True, port=4999)


#url_for usa los nombres de las funciones