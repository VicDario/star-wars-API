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

@app.route('/api/people', methods=['GET', 'POST'])
def all_people():
    if (request.method == 'GET'):
        people = People.query.all()
        people = list(map(lambda people: people.serialize(), people))
        return jsonify(people), 200

    if (request.method == 'POST'):
        name = request.json.get('name')
        height = request.json.get('height')
        mass = request.json.get('mass')
        skin_color = request.json.get('skin_color')
        eye_color = request.json.get('eye_color')
        birth_year = request.json.get('birth_year')
        gender = request.json.get('gender')

        people = People()
        people.name = name
        people.height = height
        people.mass = mass
        people.skin_color = skin_color
        people.eye_color = eye_color
        people.birth_year = birth_year
        people.gender = gender

        people.save()
        return jsonify({"Success": "created"})


@app.route('/api/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    person = list(person.serialize())
    return jsonify(person), 200

@app.route('/api/planet', methods=['GET', 'POST'])
def planets():
    if(request.method == 'GET'):
        planets = Planet.query.all()
        planets = list(map(lambda planet: planet.serialize(), planets))
        return jsonify(planets), 200

    if(request.method == 'POST'):
        name = request.json.get('name')
        diameter = request.json.get('diameter')
        rotation_period = request.json.get('rotation_period')
        orbital_period = request.json.get('orbital_period')
        gravity = request.json.get('gravity')
        population = request.json.get('population')
        climate = request.json.get('climate')
        terrain = request.json.get('terrain')
        surface_water = request.json.get('surface_water')

        planet = Planet()
        planet.name = name
        planet.diameter = diameter
        planet.rotation_period = rotation_period
        planet.orbital_period = orbital_period
        planet.gravity = gravity
        planet.population = population
        planet.climate = climate
        planet.terrain = terrain
        planet.surface_water = surface_water

        planet.save()
        return jsonify({"Success": "created"}), 201

@app.route('/api/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    planet = list(planet.serialize())
    return jsonify(planet), 200

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if(request.method == 'GET'):
        users = User.query.all()
        users = list(map(lambda user: user.serialize(), users))
        return jsonify(users), 200
    
    if(request.method == 'POST'):
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')

        user = User()
        user.username = username
        user.email = email
        user.password = password

        user.save()
        return jsonify('Success created'), 201

@app.route('/api/users/favorite', methods=['GET'])
def gets_favorite():
    favorites = Favorite.query.all()
    favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    return jsonify(favorites), 200

@app.route('/api/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
def favorite_planet(planet_id):
    if(request.method == 'POST'):
        user = User.query.get(1) 

        favorite = Favorite()
        favorite.favorite_type = "planet"
        favorite.favorite_id = planet_id
        favorite.user_id = user.id

        favorite.save()
        return jsonify("Successfully added"), 201

    if(request.method == 'DELETE'):
        planet = Favorite.query.filter_by(favorite_id=planet_id, favorite_type="planet", user_id = 1).first()
        planet.delete()
        
        return jsonify({"success": "Planet deleted from favorites"}), 200

@app.route('/api/favorite/people/<int:people_id>', methods=['POST', 'DELETE'])
def favorite_people(people_id):
    if(request.method == 'POST'):
        user = User.query.get(1) 

        favorite = Favorite()
        favorite.favorite_type = "people"
        favorite.favorite_id = people_id
        favorite.user_id = user.id

        favorite.save()

        return jsonify("Successfully added"), 201

    if(request.method == 'DELETE'):
        people = Favorite.query.filter_by(favorite_id=people_id, favorite_type="people", user_id = 1).first()
        db.session.delete(people)
        db.session.commit()

        return jsonify({ "success": "People deleted from favorites"}), 200
    
if __name__ == '__main__':
    app.run()