from flask import Blueprint, json, render_template, jsonify, request
from presenters.lewisStruct_presenter import LewisPresenter
lewis_bp = Blueprint("lewis",__name__)
presenter = LewisPresenter()

molecule = ["", [], []]
# Index and Generate H2O molecule by default
@lewis_bp.route("/", methods =["GET"])
def send_lewis():
    global molecule
    if molecule[0] != "":
        return render_template(
            "Lewis/lewis.html",
            name=molecule[0],
            nodes=molecule[1],
            edges=molecule[2]
        )
    molecule = presenter.generate_molecule("H2O")
    if not molecule:
        molecule = ["", [], []]
    return render_template(
        "Lewis/lewis.html",
        name=molecule[0],
        nodes=molecule[1],
        edges=molecule[2]
    )
# Validate molecule by name and generate nodes and edges
@lewis_bp.route("/validate", methods =["POST"])
def validate_struct():
    global molecule
    data = json.loads(request.data)
    if "name" not in data:
        return jsonify({'status': 'err', 'message': 'Faltan datos'}), 400
    name = data['name']
    if type(name) != type("hola"):
        return jsonify({'status': 'err', 'message': 'Tipo de dato inválido'}), 400
    molecule = presenter.generate_molecule(name)
    if not molecule:
        molecule = ["", [], []]
        return jsonify({'status': 'err', 'message': 'Molécula invalida o fuera del modelo'}), 400
    
    return jsonify({'status': 'ok', 'nodes': molecule[1], 'edges': molecule[2], 'name': name}), 200

#Guardar -> status ok 
@lewis_bp.route("/save", methods =["POST"])
def add_struct():
    data = json.loads(request.data)
    #print(data)
    if "name" not in data:
        return jsonify({'status': 'err', 'message': 'Faltan datos'}), 400
    if data["name"] != molecule[0]:
        return jsonify({'status': 'err', 'message': 'La molécula no coincide con la actual'}), 400
    data["nodes"] = molecule[1]
    data["edges"] = molecule[2]
    struct = presenter.create_lstruct(data)
    if struct is None:
        return jsonify({
            'status': 'duplicate',
            'message': 'La molécula ya existe.'
        }), 409
    return jsonify({'status': 'ok'}), 200

#Get all id name in a list
@lewis_bp.route("/listar")
def get_structs():
    return jsonify(presenter.get_all_structs()), 200
    #add case for empty list

# Load all data of a specific structure by name
@lewis_bp.route("/load/<string:struct_name>", methods =["GET"])
def load_struct(struct_name):
    if(struct_name.isalnum() == False):
        return jsonify({"err": "Nombre de molécula inválido"}), 400
    
    struct = presenter.get_struct_by_name(struct_name)
    if not struct:
        return jsonify({"err": "Molecula no encontrada"}), 404
    return jsonify(struct), 200
    

# Delete a specific structure by ID
@lewis_bp.route("/delete/<int:struct_id>", methods =["DELETE", "POST"])
def delete_struct(struct_id):
    if not presenter.delete_struct(struct_id):
        return jsonify({"err": "Molecula no encontrada"}), 404
    return jsonify({"ok": "Molecula eliminada"}), 200