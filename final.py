import pymongo
import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask, render_template, url_for, flash, redirect, request, abort, session, jsonify, json
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from forms import RegistrationForm, LoginForm
import bcrypt

MONGO_URI = os.getenv("MONGO_URI")
DBS_NAME = "books"
COLLECTION_NAME = "bookdetails"

"""
 This is to make a CSV file.

"""
try:
    f=open("csv.csv", "x")
except:
    print("already there")
    f=open("csv.csv", "w")

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient("mongodb+srv://12345:dude123@cluster0.x5l6q.mongodb.net")
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


conn = mongo_connect(MONGO_URI)

coll = conn[DBS_NAME][COLLECTION_NAME]

documents = coll.find()

for doc in documents: 
    print(doc, file=f)


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

@app.route("/", methods=['GET', 'POST'])
def index():
        
    return render_template('base1.html')


@app.route("/browse")
def browse():
    return render_template("browse2.html")


@app.route("/register")
def register():
    return render_template("register2.html")


@app.route("/login")
def login():
    return render_template("login3.html")


@app.route('/numbers', methods=['GET'])
def numbers():

    number = conn[DBS_NAME][COLLECTION_NAME]

    offset = int(request.args['offset'])
    limit = int(request.args['limit'])

    starting_id = number.find().sort('_id', pymongo.DESCENDING)
    last_id = starting_id[offset]['_id']

    numbers = number.find({'_id' : {'$lte' : last_id}}).sort('_id', pymongo.DESCENDING).limit(limit)

    output = []

    for i in numbers:
        output.append({'title' : i['title']})

    next_url = '/numbers?limit=' + str(limit) + '&offset' + str(offset + limit)
    prev_url = '/numbers?limit=' + str(limit) + '&offset' + str(offset - limit)

    return jsonify({'result' : output, 'prev_url' : prev_url, 'next_url' : next_url})

@app.route('/browseone', methods=['GET'])
def browseone():
    
    output =[]

    

    for i in numbers:
        output.append({'title' : i['title'] })
    
    #next_url = '/browseone?=limit' + str(limit) + '&offset=' + str(offset + limit)
    #prev_url = '/browseone?=limit' + str(limit) + '&offset=' + str(offset - limit)
    return jsonify({'result' : output, 'prev_url' : prev_url, 'next_url' : next_url})

    #return render_template("browseone1.html")

if __name__ == "__main__":
     app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)