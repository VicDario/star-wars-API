from flask import Flask, json, jsonify, request, render_template
from flask_migrate import Migrate
from models import db, People

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
db.init_app(app)
Migrate(app, db) # init, migrate, upgrade