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
  #  print(doc)


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route('/numbers', methods=['GET'])
def numbers():
    conn1a = pymongo.MongoClient("mongodb+srv://12345:dude123@cluster0.x5l6q.mongodb.net")
    number = conn1a[DBS_NAME][COLLECTION_NAME]

    numbers = coll.find().sort('bookid', pymongo.DESCENDING)
    print(numbers)
    print('justin is great')
    output = []

    for i in numbers:
        output.append({'_id' : i['numbers']})

    return jsonify({'result': output})


@app.route("/", methods=['GET', 'POST'])
def index():
        
    return render_template('base1.html')


@app.route("/bookdetails", methods=['GET','POST'])
def bookdetails():

    return render_template('bookdetails.html')

if __name__ == "__main__":
     app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)