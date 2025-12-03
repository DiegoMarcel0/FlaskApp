from models.TreasureLand import Grafo, db

class TreasureLandPresenter:
    #Guardar -> status ok +id
    def create_grafo(self, data):
        new_grafo = Grafo(**data)
        db.session.add(new_grafo)
        db.session.commit()
        return new_grafo
    
    
    #Get all id nombre ->list
    def get_all_grafos(self):
        return Grafo.query.with_entities(Grafo.id, Grafo.nombre).all()
        
    
    #Load JSON(size, start, end, walls)
    def get_grafo_by_id(self, id_grafo):
        return Grafo.query.get(id_grafo).__dict__