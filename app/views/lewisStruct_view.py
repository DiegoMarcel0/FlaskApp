from flask import Blueprint, render_template
import networkx as nx
from views.lewis.Lewis import estructura_lewis
lewis_bp = Blueprint("lewis",__name__)
#presenter = LewisPresenter()


@lewis_bp.route("/", methods =["GET"])
def send_lewis():
    molecula_grafo = estructura_lewis("H2O")
    pos = nx.kamada_kawai_layout(molecula_grafo)
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
    return render_template(
        "Lewis/lewis.html",
        nodes=nodes,
        edges=edges
    )

