from models.lewisStruct import LStructureModel
from views.lewis.Lewis import estructura_lewis

model = LStructureModel()
class LewisPresenter:
    def __init__(self):
        self.model = LStructureModel()
    #Save a new Lewis structure
    def create_lstruct(self, data):
        if self.model.exists_name(data["name"]):
            return None
        struct = self.model.create(data)
        return struct

    #Get all {id name} -> list
    def get_all_structs(self):
        structs = self.model.get_all()
        return [{"id": struct.id, "name": struct.name} for struct in structs]

    #Load JSON(NODES & EDGES) by name
    def get_struct_by_name(self, name_struct):
        struct = self.model.get_by_name(name_struct)
        if not struct:
            return None
        return {
            'status': 'ok',
            'name': struct["name"],
            'nodes': struct["nodes"],
            'edges': struct["edges"]
        }
    
    #Delete a specific structure by ID
    def delete_struct(self, id_struct):
        return self.model.delete(id_struct)
    
    #Generate molecule by name and return nodes and edges
    def generate_molecule(self, name):
        pos, molecula_grafo = estructura_lewis(name)
        if not molecula_grafo:
            return None
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
        return [name, nodes, edges]