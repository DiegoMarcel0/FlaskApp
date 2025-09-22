from models.helloMySQL import Empleado, db

class EmpleadoPresenter:
    def create_empleado(self, data):
        new_empleado = Empleado(**data)
        db.session.add(new_empleado)
        db.session.commit()
        return new_empleado
    
    def get_all_empleados(self):
        return Empleado.query.with_entities(Empleado.id, Empleado.name, Empleado.email, Empleado.sumary).all()
    
    def get_empleado_by_id(self, id_empleado):
        return Empleado.query.get(id_empleado).__dict__
    
    def update_empleado(self, id_empleado, data):
        empleado = Empleado.query.get(id_empleado)
        #print(empleado)
        if not empleado:
            return None
        for key, value in data.items():
            if hasattr(empleado, key):
                setattr(empleado, key, value)
        db.session.commit()
        return empleado
    def delete_empleado(self, id_empleado):
        empleado = Empleado.query.get(id_empleado)
        if not empleado:
            return None
        db.session.delete(empleado)
        db.session.commit()
        return empleado
        