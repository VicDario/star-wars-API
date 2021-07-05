import dotenv
from dotenv.main import dotenv_values
from flask import Flask, json, jsonify, request, render_template
from flask_migrate import Migrate
from models import Favorite, Planet, Specie, Starship, User, db, People
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")

db.init_app(app)
Migrate(app, db) # init, migrate, upgrade

jwt = JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

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

@app.route('/api/specie', methods=['GET', 'POST'])
def species():
    if(request.method == 'GET'):
        species = Specie.query.all()
        species = list(map(lambda specie: specie.serialize(), species))
        return jsonify(species), 200

    if(request.method == 'POST'):
        name = request.json.get('name')
        classification = request.json.get('classification')
        designation = request.json.get('designation')
        average_height = request.json.get('average_height')
        average_lifespan = request.json.get('average_lifespan')
        hair_colors = request.json.get('hair_colors')
        skin_colors = request.json.get('skin_colors')
        eye_colors = request.json.get('eye_colors')
        homeworld = request.json.get('homeworld')
        language = request.json.get('language')

        specie = Specie()
        specie.name = name
        specie.classification = classification
        specie.designation = designation
        specie.average_height = average_height
        specie.average_lifespan = average_lifespan
        specie.hair_colors = hair_colors
        specie.skin_colors = skin_colors
        specie.eye_colors = eye_colors
        specie.homeworld = homeworld
        specie.language = language

        specie.save()
        return jsonify({"Success": "created"}), 201

@app.route('/api/specie/<int:specie_id>', methods=['GET'])
def get_specie(specie_id):
    specie = Specie.query.get(specie_id)
    specie = list(specie.serialize())
    return jsonify(specie), 200

@app.route('/api/starship', methods=['GET', 'POST'])
def starships():
    if(request.method == 'GET'):
        starships = Starship.query.all()
        starships = list(map(lambda starship: starship.serialize(), starships))
        return jsonify(starships), 200

    if(request.method == 'POST'):
        name = request.json.get('name')
        model = request.json.get('model')
        starship_class = request.json.get('starship_class')
        manufacturer = request.json.get('manufacturer')
        cost_in_credits = request.json.get('cost_in_credits')
        length = request.json.get('length')
        crew = request.json.get('crew')
        passengers = request.json.get('passengers')
        max_atmosphering_speed = request.json.get('max_atmosphering_speed')
        hyperdrive_rating = request.json.get('hyperdrive_rating')
        MGLT = request.json.get('MGLT')
        cargo_capacity = request.json.get('cargo_capacity')
        consumables = request.json.get('consumables')

        starship = Starship()
        starship.name = name
        starship.model = model
        starship.starship_class = starship_class
        starship.manufacturer = manufacturer
        starship.cost_in_credits = cost_in_credits
        starship.length = length
        starship.crew = crew
        starship.passengers = passengers
        starship.max_atmosphering_speed = max_atmosphering_speed
        starship.hyperdrive_rating = hyperdrive_rating
        starship.MGLT = MGLT
        starship.cargo_capacity = cargo_capacity
        starship.consumables = consumables

        starship.save()
        return jsonify({"Success": "created"}), 201

@app.route('/api/starship/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):
    starship = Starship.query.get(starship_id)
    starship = list(starship.serialize())
    return jsonify(starship), 200


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
def get_favorites():
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
        favorite = Favorite.query.filter_by(favorite_id=planet_id, favorite_type="planet", user_id = 1).first()
        favorite.delete()
        
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
        favorite = Favorite.query.filter_by(favorite_id=people_id, favorite_type="people", user_id = 1).first()
        favorite.delete()

        return jsonify({ "success": "People deleted from favorites"}), 200

app.route('/api/favorite/specie/<int:specie_id>', methods=['POST', 'DELETE'])
def favorite_specie(specie_id):
    if(request.method == 'POST'):
        user = User.query.get(1) 

        favorite = Favorite()
        favorite.favorite_type = "specie"
        favorite.favorite_id = specie_id
        favorite.user_id = user.id

        favorite.save()

        return jsonify("Successfully added"), 201

    if(request.method == 'DELETE'):
        favorite = Favorite.query.filter_by(favorite_id=specie_id, favorite_type="specie", user_id = 1).first()
        favorite.delete()

        return jsonify({ "success": "Specie deleted from favorites"}), 200

app.route('/api/favorite/starship/<int:starship_id>', methods=['POST', 'DELETE'])
def favorite_starship(starship_id):
    if(request.method == 'POST'):
        user = User.query.get(1) 

        favorite = Favorite()
        favorite.favorite_type = "specie"
        favorite.favorite_id = starship_id
        favorite.user_id = user.id

        favorite.save()

        return jsonify("Successfully added"), 201

    if(request.method == 'DELETE'):
        favorite = Favorite.query.filter_by(favorite_id=starship_id, favorite_type="starship", user_id = 1).first()
        favorite.delete()

        return jsonify({ "success": "Starship deleted from favorites"}), 200
    
if __name__ == '__main__':
    app.run()