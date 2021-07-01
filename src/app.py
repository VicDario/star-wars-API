from flask import Flask, json, jsonify, request, render_template
from flask_migrate import Migrate
from models import Planet, db, People

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
db.init_app(app)
Migrate(app, db) # init, migrate, upgrade

@app.route('/people', methods=['GET'])
def all_people():
    people = People.query.all()
    people = list(map(lambda people: people.serialize(), people))
    return jsonify(people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    person = list(person.serialize())
    return jsonify(person), 200

@app.route('/planet', methods=['GET'])
def all_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    planet = list(planet.serialize())
    return jsonify(planet), 200