from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from flask import Flask, jsonify, request
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
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db.init_app(app)
Migrate(app, db)  # init, migrate, upgrade

jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).first()        
    if user is not None and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"Error": "Bad username or password"}), 401

@app.route('/api/people', methods=['GET', 'POST'])
def all_people():
    if (request.method == 'GET'):
        people = People.query.all()
        people = list(map(lambda people: people.serialize(), people))
        return jsonify(people), 200

    if (request.method == 'POST'):
        people = People()
        people.name = request.json.get('name')
        people.height = request.json.get('height')
        people.mass = request.json.get('mass')
        people.skin_color = request.json.get('skin_color')
        people.eye_color = request.json.get('eye_color')
        people.birth_year = request.json.get('birth_year')
        people.gender = request.json.get('gender')

        people.save()
        return jsonify({"Success": "created"})


@app.route('/api/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    person = list(person.serialize())
    return jsonify(person), 200


@app.route('/api/people/<int:people_id>', methods=['PUT'])
@jwt_required()
def put_people(people_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).one_or_none()
    if user.id == 1:
        people = People.query.get(people_id)

        people.name = request.json.get('name', people.name)
        people.height = request.json.get('height', people.height)
        people.mass = request.json.get('mass', people.mass)
        people.skin_color = request.json.get('skin_color', people.skin_color)
        people.eye_color = request.json.get('eye_color', people.eye_color)
        people.birth_year = request.json.get('birth_year', people.birth_year)
        people.gender = request.json.get('gender', people.gender)

        people.update()
        return jsonify({"Success": "Changes apply"})
    else:
        return jsonify({"Error": "You don´t have permissions for this"})


@app.route('/api/planet', methods=['GET', 'POST'])
def planets():
    if(request.method == 'GET'):
        planets = Planet.query.all()
        planets = list(map(lambda planet: planet.serialize(), planets))
        return jsonify(planets), 200

    if(request.method == 'POST'):
        planet = Planet()
        planet.name = request.json.get('name')
        planet.diameter = request.json.get('diameter')
        planet.rotation_period = request.json.get('rotation_period')
        planet.orbital_period = request.json.get('orbital_period')
        planet.gravity = request.json.get('gravity')
        planet.population = request.json.get('population')
        planet.climate = request.json.get('climate')
        planet.terrain = request.json.get('terrain')
        planet.surface_water = request.json.get('surface_water')

        planet.save()
        return jsonify({"Success": "created"}), 201


@app.route('/api/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    planet = list(planet.serialize())
    return jsonify(planet), 200


@app.route('/api/planet/<int:planet_id>', methods=['PUT'])
@jwt_required()
def put_planet(planet_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).one_or_none()
    if user.id == 1:
        planet = Planet.query.get(planet_id)

        planet.name = request.json.get('name', planet.name)
        planet.diameter = request.json.get('diameter',  planet.diameter)
        planet.rotation_period = request.json.get('rotation_period', planet.rotation_period)
        planet.orbital_period = request.json.get('orbital_period', planet.orbital_period)
        planet.gravity = request.json.get('gravity', planet.gravity)
        planet.population = request.json.get('population', planet.population)
        planet.climate = request.json.get('climate', planet.climate)
        planet.terrain = request.json.get('terrain', planet.terrain)
        planet.surface_water = request.json.get('surface_water', planet.surface_water)

        planet.update()
        return jsonify({"Success": "Changes apply"}), 202
    else:
        return jsonify({"Error": "You don´t have permissions for this"}), 402


@app.route('/api/specie', methods=['GET', 'POST'])
def species():
    if(request.method == 'GET'):
        species = Specie.query.all()
        species = list(map(lambda specie: specie.serialize(), species))
        return jsonify(species), 200

    if(request.method == 'POST'):
        specie = Specie()
        specie.name = request.json.get('name')
        specie.classification = request.json.get('classification')
        specie.designation = request.json.get('designation')
        specie.average_height = request.json.get('average_height')
        specie.average_lifespan = request.json.get('average_lifespan')
        specie.hair_colors = request.json.get('hair_colors')
        specie.skin_colors = request.json.get('skin_colors')
        specie.eye_colors = request.json.get('eye_colors')
        specie.homeworld = request.json.get('homeworld')
        specie.language = request.json.get('language')

        specie.save()
        return jsonify({"Success": "created"}), 201


@app.route('/api/specie/<int:specie_id>', methods=['GET'])
def get_specie(specie_id):
    specie = Specie.query.get(specie_id)
    specie = list(specie.serialize())
    return jsonify(specie), 200


@app.route('/api/specie/<int:specie_id>', methods=['PUT'])
@jwt_required()
def put_specie(specie_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).one_or_none()
    if user.id == 1:
        specie = Specie.query.get(specie_id)

        specie.name = request.json.get('name', specie.name)
        specie.classification = request.json.get('classification', specie.classification)
        specie.designation = request.json.get('designation', specie.designation)
        specie.average_height = request.json.get('average_height', specie.average_height)
        specie.average_lifespan = request.json.get('average_lifespan', specie.average_lifespan)
        specie.hair_colors = request.json.get('hair_colors', specie.hair_colors)
        specie.skin_colors = request.json.get('skin_colors', specie.skin_colors)
        specie.eye_colors = request.json.get('eye_colors', specie.eye_colors)
        specie.homeworld = request.json.get('homeworld', specie.homeworld)
        specie.language = request.json.get('language', specie.language)

        specie.update()
        return jsonify({"Success": "Changes apply"}), 202
    else:
        return jsonify({"Error": "You don´t have permissions for this"}), 402


@app.route('/api/starship', methods=['GET', 'POST'])
def starships():
    if(request.method == 'GET'):
        starships = Starship.query.all()
        starships = list(map(lambda starship: starship.serialize(), starships))
        return jsonify(starships), 200

    if(request.method == 'POST'):
        starship = Starship()
        starship.name = request.json.get('name')
        starship.model = request.json.get('model')
        starship.starship_class = request.json.get('starship_class')
        starship.manufacturer = request.json.get('manufacturer')
        starship.cost_in_credits = request.json.get('cost_in_credits')
        starship.length = request.json.get('length')
        starship.crew = request.json.get('crew')
        starship.passengers = request.json.get('passengers')
        starship.max_atmosphering_speed = request.json.get('max_atmosphering_speed')
        starship.hyperdrive_rating = request.json.get('hyperdrive_rating')
        starship.MGLT = request.json.get('MGLT')
        starship.cargo_capacity = request.json.get('cargo_capacity')
        starship.consumables = request.json.get('consumables')

        starship.save()
        return jsonify({"Success": "created"}), 201


@app.route('/api/starship/<int:starship_id>', methods=['GET'])
def get_starship(starship_id):
    starship = Starship.query.get(starship_id)
    starship = list(starship.serialize())
    return jsonify(starship), 200


@app.route('/api/startship/<int:starship_id>', methods=['PUT'])
@jwt_required()
def put_starship(starship_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).one_or_none()
    if user.id == 1:
        starship = Starship.query.get(starship_id)

        starship.name = request.json.get('name', starship.name)
        starship.model = request.json.get('model', starship.model)
        starship.starship_class = request.json.get('starship_class', starship.starship_class)
        starship.manufacturer = request.json.get('manufacturer', starship.manufacturer)
        starship.cost_in_credits = request.json.get('cost_in_credits', starship.cost_in_credits)
        starship.length = request.json.get('length', starship.length)
        starship.crew = request.json.get('crew', starship.crew)
        starship.passengers = request.json.get('passengers', starship.passengers)
        starship.max_atmosphering_speed = request.json.get('max_atmosphering_speed', starship.max_atmosphering_speed)
        starship.hyperdrive_rating = request.json.get('hyperdrive_rating', starship.hyperdrive_rating)
        starship.MGLT = request.json.get('MGLT', starship.MGLT)
        starship.cargo_capacity = request.json.get('cargo_capacity', starship.cargo_capacity)
        starship.consumables = request.json.get('consumables', starship.consumables)

        starship.update()
        return jsonify({"Success": "Changes apply"})
    else:
        return jsonify({"Error": "You don´t have permissions for this"}), 402


@app.route('/api/user/register', methods=['POST'])
def users():
    if(request.method == 'POST'):
        user = User()
        user.username = request.json.get('username')
        user.email = request.json.get('email')
        user.password = generate_password_hash(request.json.get('password'))

        user.save()
        return jsonify('Success created'), 201

@app.route('/api/user', methods=['GET'])
@jwt_required()
def user_info():
    pass

@app.route('/api/users/favorite', methods=['GET'])
@jwt_required()
def get_favorites():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).one_or_none()
    if user is None:
        return jsonify({"Error": "No valid user"})
    return jsonify(User.serialize_favorites(user)), 200


@app.route('/api/favorite/planet/<int:planet_id>', methods=['POST', 'DELETE'])
@jwt_required()
def favorite_planet(planet_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).one_or_none()
    if(request.method == 'POST'):
        planet = Planet.query.get(planet_id)
        if planet is None:
            return jsonify({"Error": "Item not founded"}), 403
        favorite = Favorite()
        favorite.favorite_type = "planet"
        favorite.favorite_id = planet_id
        favorite.user_id = user.id

        favorite.save()
        return jsonify("Successfully added"), 201

    if(request.method == 'DELETE'):
        favorite = Favorite.query.filter_by(
            favorite_id=planet_id, favorite_type="planet", user_id=user.id).first()
        favorite.delete()

        return jsonify({"success": "Planet deleted from favorites"}), 200


@app.route('/api/favorite/people/<int:people_id>', methods=['POST', 'DELETE'])
@jwt_required()
def favorite_people(people_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).one_or_none()
    if(request.method == 'POST'):
        people = People.query.get(people_id)
        if people is None:
            return jsonify({"Error": "Item not founded"}), 403
        favorite = Favorite()
        favorite.favorite_type = "people"
        favorite.favorite_id = people_id
        favorite.user_id = user.id

        favorite.save()

        return jsonify("Successfully added"), 201

    if(request.method == 'DELETE'):
        favorite = Favorite.query.filter_by(
            favorite_id=people_id, favorite_type="people", user_id=user.id).first()
        favorite.delete()

        return jsonify({"success": "People deleted from favorites"}), 200


app.route('/api/favorite/specie/<int:specie_id>', methods=['POST', 'DELETE'])


@jwt_required()
def favorite_specie(specie_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).one_or_none()
    if(request.method == 'POST'):
        specie = Specie.query.get(specie_id)
        if specie is None:
            return jsonify({"Error": "Item not founded"}), 403
        favorite = Favorite()
        favorite.favorite_type = "specie"
        favorite.favorite_id = specie_id
        favorite.user_id = user.id

        favorite.save()

        return jsonify("Successfully added"), 201

    if(request.method == 'DELETE'):
        favorite = Favorite.query.filter_by(
            favorite_id=specie_id, favorite_type="specie", user_id=user.id).first()
        favorite.delete()

        return jsonify({"success": "Specie deleted from favorites"}), 200


app.route('/api/favorite/starship/<int:starship_id>',
          methods=['POST', 'DELETE'])


def favorite_starship(starship_id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).one_or_none()
    if(request.method == 'POST'):
        starship = Starship.query.get(starship_id)
        if starship is None:
            return jsonify({"Error": "Item not founded"}), 403
        favorite = Favorite()
        favorite.favorite_type = "starship"
        favorite.favorite_id = starship_id
        favorite.user_id = user.id

        favorite.save()

        return jsonify("Successfully added"), 201

    if(request.method == 'DELETE'):
        favorite = Favorite.query.filter_by(
            favorite_id=starship_id, favorite_type="starship", user_id=user.id).first()
        favorite.delete()

        return jsonify({"success": "Starship deleted from favorites"}), 200


if __name__ == '__main__':
    app.run()
