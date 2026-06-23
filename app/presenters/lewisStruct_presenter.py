from models.lewisStruct import LStructure, db

class LewisPresenter:
    #Guardar -> status ok +id
    def create_lstruct(self, data):
        new_struct = LStructure(**data)
        db.session.add(new_struct)
        db.session.commit()
        return new_struct
    
    
    #Get all id nombre ->list
    def get_all_structs(self):
        return LStructure.query.with_entities(LStructure.id, LStructure.nombre).all()
        
    
    #Load JSON(NODES & EDGES)
    def get_struct_by_id(self, id_struct):
        return LStructure.query.get(id_struct).__dict__


    def delete_struct(self, id_struct):
        struct = LStructure.query.get(id_struct)
        if not struct:
            return None
        db.session.delete(struct)
        db.session.commit()
        return struct