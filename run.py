import pymongo
import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask, render_template, url_for, flash, redirect, request, abort, session, jsonify, json


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
        conn = pymongo.MongoClient("mongodb+srv://12345:dude123@cluster0.x5l6q.mongodb.net/books")
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


conn = mongo_connect(MONGO_URI)

coll = conn[DBS_NAME][COLLECTION_NAME]

documents = coll.find()

for doc in documents: 
    print(doc, file=f)


app = Flask(__name__)


@app.route('/')
def index():
    if 'username' in session:
        return 'Hi there' + session['username']
    return render_template("index.html")


@app.route('/browse')
def browse():
    return render_template("browse.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/login')
def login():

    return render_template("login.html")


@app.route('/csv.csv')
def csv():
    return render_template("csv.csv")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
