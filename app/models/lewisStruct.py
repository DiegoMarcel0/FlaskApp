from extensions import db

class LStructure(db.Model):
    __tablename__ = "lewis_structure"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    nodes = db.Column(db.JSON)   # JSON compatible con MySQL
    edges = db.Column(db.JSON)
    def to_dict(self):
        return {
            "name": self.name,
            "nodes": self.nodes,
            "edges": self.edges
        }

class LStructureModel:
    #Guardar -> status ok + id
    def create(self, data):
        new_struct = LStructure(**data)
        db.session.add(new_struct)
        db.session.commit()
        return new_struct
     
    #Get all id nombre ->list
    def get_all(self):
        return LStructure.query.with_entities(LStructure.id, LStructure.name).all()
        
    
    #Load JSON(NODES & EDGES) by name
    def get_by_name(self, name_struct):
        return LStructure.query.filter_by(name=name_struct).first().to_dict()
        #return LStructure.query.get(name_struct).to_dict()
    
    def exists_name(self, name_struct):
        return LStructure.query.filter_by(name=name_struct).first() is not None
    
    #Delete a specific structure by ID
    def delete(self, id_struct):
        struct = LStructure.query.get(id_struct)
        if not struct:
            return None
        db.session.delete(struct)
        db.session.commit()
        return struct

    def get_all(self):
        return LStructure.query.all()
