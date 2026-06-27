from flask import Blueprint, json, render_template, jsonify, request
from views.lewis.Lewis import estructura_lewis
from sqlalchemy.exc import IntegrityError
from presenters.lewisStruct_presenter import LewisPresenter
lewis_bp = Blueprint("lewis",__name__)
presenter = LewisPresenter()

nodes = edges = []
moleculeName = "H2O"
@lewis_bp.route("/", methods =["GET"])
def send_lewis():
    global nodes
    global edges
    if nodes != [] or edges != []:
        return render_template(
            "Lewis/lewis.html",
            name=moleculeName,
            nodes=nodes,
            edges=edges
        )
    pos, molecula_grafo = estructura_lewis(moleculeName)
    nodes = []
    for node, data in molecula_grafo.nodes(data=True):
        print("node: ", node, "data: ", data)
        nodes.append({
            "id": node,
            "elemento": data["elemento"],
            "free_atoms": data["free_atoms"],
            "x": float(pos[node][1]),
            "y": float(pos[node][0])
            })
    edges = []
    for u, v, data in molecula_grafo.edges(data=True):
        edges.append({
            "source": u,
            "target": v,
            "weight": data["weight"]
        })
    return render_template(
        "Lewis/lewis.html",
        nodes=nodes,
        edges=edges,
        name=moleculeName
    )

@lewis_bp.route("/validate", methods =["POST"])
def validate_struct():
    global nodes
    global edges
    global moleculeName
    data = json.loads(request.data)
    name = data['name']
    if type(name) == type("hola"):
        pos, molecula_grafo = estructura_lewis(name)
    else:
        print("What the hell is this")
        print(name)
        return jsonify({'status': 'err'})
    if molecula_grafo == None:
        return jsonify({'status': 'err'})

    nodes = []
    for node, data in molecula_grafo.nodes(data=True):
        nodes.append({
            "id": node,
            "elemento": data["elemento"],
            "free_atoms": data["free_atoms"],
            "x": float(pos[node][1]),
            "y": float(pos[node][0])
            })
    edges = []
    for u, v, data in molecula_grafo.edges(data=True):
        edges.append({
            "source": u,
            "target": v,
            "weight": data["weight"]
        })
    moleculeName = name
    return jsonify({'status': 'ok', 'nodes': nodes, 'edges': edges, 'name': name})

#Guardar -> status ok +id
@lewis_bp.route("/save", methods =["POST"])
def add_struct():
    data = json.loads(request.data)
    #print(data)
    if "name" not in data:
        return jsonify({'status': 'err', 'message': 'Missing required fields'}), 400
    if data["name"] != moleculeName:
        return jsonify({'status': 'err', 'message': 'Molecule name does not match the current molecule'}), 400
        #return jsonify({'status': 'err', 'message': 'Cannot save the same molecule'}), 400
    data["nodes"] = nodes
    data["edges"] = edges
    try:
        struct = presenter.create_lstruct(data)
        return jsonify({'status': 'ok', 'id': struct.id, 'name': struct.name})
    except IntegrityError:
        return jsonify({
            'status': 'duplicate',
            'message': 'La molécula ya existe.'
        }), 409
    except Exception as e:
        print("Error saving structure:", type(e).__cause__)
        return jsonify({'status': 'err', 'message': str(e)}), 400

#Get all id name ->list
@lewis_bp.route("/listar")
def get_structs():
    structs = presenter.get_all_structs()
    return jsonify([{"id": t[0], "name": t[1]} for t in structs])

# Load all data of a specific structure by ID
@lewis_bp.route("/load/<string:struct_name>", methods =["GET"])
def load_struct(struct_name):
    try:
        struct = presenter.get_struct_by_name(struct_name)
        return jsonify({
            'status': 'ok',
            'name': struct["name"],
            'nodes': struct["nodes"],
            'edges': struct["edges"]
        })
    except Exception as e:
        print("Error loading structure:", type(e).__cause__)
        return jsonify({'status': 'err', 'message': str(e)}), 400
    

# Delete a specific structure by ID
@lewis_bp.route("/delete/<int:struct_id>", methods =["DELETE", "POST"])
def delete_struct(struct_id):
    #return redirect(url_for("empleado.list_empleados"))
    struct = presenter.delete_struct(struct_id)
    if not struct:
        return jsonify({"err": "Molecula no encontrado"}), 404
    return jsonify({"ok": "Molecula eliminada"}), 200