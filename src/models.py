from enum import unique
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    height = db.Column(db.String(4), nullable=False)
    mass = db.Column(db.String(4), nullable=False)
    skin_color = db.Column(db.String(10))
    eye_color = db.Column(db.String(10))
    birth_year = db.Column(db.String(10))
    gender = db.Column(db.String(6))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(id.String(25), unique=True)
    diameter = db.Column(db.Integer, nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    gravity = db.Column(db.String(15), nullable=False)
    population = db.Column(db.Integer, nullable=False)
    climate = db.Column(db.String(20), nullable=False)
    terrain = db.Column(db.String(30), nullable=False)
    surface_water = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }