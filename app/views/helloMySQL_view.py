from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from presenters.helloMySQL_presenter import EmpleadoPresenter

empleado_bp = Blueprint("empleado",__name__)
presenter = EmpleadoPresenter()

@empleado_bp.route("/insertar", methods =["GET"])
def insertar():
    return render_template('helloMySQL/insertar.html')

@empleado_bp.route("/insertar", methods =["POST"])
def add_empleado():
    data = request.form
    #print(data)
    empleado = presenter.create_empleado(data)
    #print(empleado)
    return redirect(url_for("empleado.list_empleados"))

@empleado_bp.route("/")
def list_empleados():
    empleados = presenter.get_all_empleados()
    return render_template("helloMySQL/datos.html", data = empleados)

@empleado_bp.route("/<int:id_empleado>/editar", methods =["GET"])
def edit_empleado(id_empleado):
    empleado = presenter.get_empleado_by_id(id_empleado)
    #print(empleado)
    return render_template("helloMySQL/editar.html", data = empleado)

@empleado_bp.route("/<int:id_empleado>/editar", methods = ["PUT", "POST"])
def update_empleado(id_empleado):
    data = request.form
    empleado = presenter.update_empleado(id_empleado, data)
    if not empleado:
        return jsonify({"error": "Empleado no encontrado"}), 404
    return redirect(url_for("empleado.list_empleados"))

    

@empleado_bp.route("/<int:id_empleado>/eliminar", methods =["DELETE", "POST"])
def delete_empleado(id_empleado):
    #return redirect(url_for("empleado.list_empleados"))
    empleado = presenter.delete_empleado(id_empleado)
    if not empleado:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return redirect(url_for("empleado.list_empleados")) 