from flask_jwt_extended import JWTManager
from pymongo import MongoClient

mongo = MongoClient("mongodb+srv://lucascostx:slzsUXzALaeWy1U3@cluster0.dgz2h.mongodb.net/")
db = mongo.estoquePro
jwt = JWTManager()