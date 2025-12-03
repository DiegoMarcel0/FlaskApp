from extensions import db

class Grafo(db.Model):
    __tablename__ = "grafo"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, default=10)

    inicio = db.Column(db.JSON)   # JSON compatible con MySQL
    fin = db.Column(db.JSON)
    muros = db.Column(db.JSON)    # lista de coordenadas [[x, y], ...]


    def __repr__(self):
        return f"<Grafo {self.nombre}>"
    def to_dict(self):
        return {c.nombre: getattr(self, c.nombre) for c in self.__table__.columns}
