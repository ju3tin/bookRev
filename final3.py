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

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

conn = pymongo.MongoClient("mongodb+srv://12345:dude123@cluster0.x5l6q.mongodb.net")
DBS_NAME = "books"
COLLECTION_NAME = "bookdetails"

coll = conn[DBS_NAME]


mongo = coll


@app.route("/", methods=['GET', 'POST'])
def index():
        
    return render_template('base1.html')

@app.route('/numbers', methods=['GET'])
def numbers():
    conn1a = pymongo.MongoClient("mongodb+srv://12345:dude123@cluster0.x5l6q.mongodb.net")
    number = conn1a.books.bookdetails1

    numbers = number.find().sort('bookid', pymongo.DESCENDING)
    print(numbers)
    print('justin is great')
    output = []

    for s in numbers:
        output.append({'title' : s['title'],'descripton' : s['descripton'], 'isbn' : s['isbn'], 'authors': s['authors'], 'publication_date': s['publication_date'], 'publisher': s['publisher']})
        
    #return jsonify({'result': output})
    return render_template('browse3.html', output=output)


@app.route('/star', methods=['GET'])
def get_all_stars():
  star = coll.bookdetails1
  output = []
  for s in star.find():
    output.append({'title' : s['title'],'descripton' : s['descripton'], 'isbn' : s['isbn'], 'authors': s['authors'], 'publication_date': s['publication_date'], 'publisher': s['publisher']})
    return jsonify({'result' : output})
    #return render_template('browse3.html', output=output)

@app.route('/star/', methods=['GET'])
def get_one_star(name):
  star = coll.bookdetails
  s = star.find_one({'name' : name})
  if s:
    output = {'name' : s['name'], 'distance' : s['distance']}
  else:
    output = "No such name"
  return jsonify({'result' : output})

@app.route('/star', methods=['POST'])
def add_star():
  star = coll.bookdetails
  name = request.json['name']
  distance = request.json['distance']
  star_id = star.insert({'name': name, 'distance': distance})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'distance' : new_star['distance']}
  return jsonify({'result' : output})

if __name__ == '__main__':
     app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)