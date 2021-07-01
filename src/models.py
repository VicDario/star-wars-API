from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(4), nullable=False)
    mass = db.Column(db.String(4), nullable=False)
    skin_color = db.Column(db.String(10))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color
        }