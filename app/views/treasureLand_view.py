import heapq
from flask import Blueprint, json, jsonify, redirect, render_template, request, url_for
from presenters.treasureLand_presenter import TreasureLandPresenter
import networkx as nx

treasureLand_bp = Blueprint("treasureLand",__name__)
presenter = TreasureLandPresenter()
#/
@treasureLand_bp.route("/")
def list_empleados():
    return redirect(url_for("treasureLand.grilla_con_obstaculos"))
#Principal
@treasureLand_bp.route("/grilla", methods =["GET"])
def grilla_con_obstaculos():
    return render_template("Treasure/grilla_astar.html", size =10)

#Guardar -> status ok +id
@treasureLand_bp.route("/guardar-grafo", methods =["POST"])
def add_grafo():
    data = json.loads(request.data)
    print(data)
    grafo = presenter.create_grafo(data)
    print(grafo)
    return jsonify({'status': 'ok', 'grafo_id': grafo.id})
    #return render_template("Treasure/grilla_astar.html", size =10)

#Get all id nombre ->list
@treasureLand_bp.route("/listar-grafos")
def obtener_grafos():
    grafos = presenter.get_all_grafos()
    print(grafos)
    #return "hola"
    return jsonify([{"id": t[0], "nombre": t[1]} for t in grafos])
    return jsonify([list(g) for g in grafos])
    #return jsonify(grafos)

#load get JSON(size, start, end, walls)
@treasureLand_bp.route("/cargar-grafo/<int:grafo_id>", methods =["GET"])
def cargar_grafo(grafo_id):
    grafo = presenter.get_grafo_by_id(grafo_id)
    print(grafo)
    return jsonify({
            'size': grafo["size"],
            'start': grafo["inicio"],
            'end': grafo["fin"],
            'walls': grafo["muros"]
        })

#RESOLVER ASTAR
@treasureLand_bp.route("/resolver-astar", methods = ["PUT", "POST"])
def resolver_astar():
    data = json.loads(request.data)
    size = data['size']
    start = tuple(data['start'])
    end = tuple(data['end'])
    walls = [tuple(w) for w in data['walls']]
    heuristica = data.get('heuristica', 'manhattan')

    G = nx.grid_2d_graph(size, size)
    for wall in walls:
        G.remove_node(wall)

    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def euclidiana(a, b):
        return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

    def chebyshev(a, b):
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
    def zero(a, b):
        return 0
    # Elegir heurística
    if heuristica == 'manhattan':
        h = manhattan
    elif heuristica == 'euclidiana':
        h = euclidiana
    elif heuristica == 'chebyshev':
        h = chebyshev
    elif heuristica == 'zero':
        h = zero
    else:
        h = manhattan  # Default
        print("watafa amigo, vos estas reloco")

    # A* con heurística seleccionada
    open_set = [(0 + h(start, end), 0, start)]
    came_from = {}
    g_score = {start: 0}
    visitados = []

    while open_set:
        _, cost, current = heapq.heappop(open_set)

        visitados.append(current)
        if current == end:
            break

        for neighbor in G.neighbors(current):
            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + h(neighbor, end)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    path = []
    current = end
    while current in came_from:
        path.append(current)
        current = came_from[current]
    if path:
        path.append(start)
        path.reverse()

    return jsonify({
        'visitados': visitados,
        'camino': path
    })
