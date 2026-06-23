from extensions import db

class LStructure(db.Model):
    __tablename__ = "lewis_structure"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    nodes = db.Column(db.JSON)   # JSON compatible con MySQL
    edges = db.Column(db.JSON)
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
