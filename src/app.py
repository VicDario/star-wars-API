from flask import Flask, json, jsonify, request, render_template
from flask_migrate import Migrate
from models import Favorite, Planet, User, db, People

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
db.init_app(app)
Migrate(app, db) # init, migrate, upgrade

@app.route('/api/people', methods=['GET'])
def all_people():
    people = People.query.all()
    people = list(map(lambda people: people.serialize(), people))
    return jsonify(people), 200

@app.route('api/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    person = list(person.serialize())
    return jsonify(person), 200

@app.route('/api/planet', methods=['GET'])
def all_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))
    return jsonify(planets), 200

@app.route('/api/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    planet = list(planet.serialize())
    return jsonify(planet), 200

@app.route('/api/users', methods=['GET'])
def all_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))
    return jsonify(users), 200

@app.route('/api/users/favorite', methods=['GET'])
def gets_favorite():
    favorites = Favorite.query.all()
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(favorites), 200

@app.route('/api/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_to_favorite(planet_id):
    favorite = Favorite()
    favorite.favorite_type = "planet"
    favorite.favorite_id = planet_id

    db.session.add(favorite)
    db.session.commit()

    return jsonify("Successfully added"), 201

@app.route('/api/favorite/people/<int:people_id>', methods=['POST'])
def add_people_to_favorite(people_id):
    favorite = Favorite()
    favorite.favorite_type = "people"
    favorite.favorite_id = people_id

    db.session.add(favorite)
    db.session.commit()

    return jsonify("Successfully added"), 201

@app.route('/api/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_at_favorites(planet_id):
    planet = Planet.query.get(planet_id)
    db.session.delete(planet)
    db.session.commit()

    return jsonify({ "success": "Planet deleted from favorites"}), 200

@app.route('/api/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_planet_at_favorites(planet_id):
    people = People.query.get(planet_id)
    db.session.delete(people)
    db.session.commit()

    return jsonify({ "success": "People deleted from favorites"}), 200

if __name__ == '__main__':
    app.run()