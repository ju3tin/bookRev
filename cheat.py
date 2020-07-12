import pymongo
import os
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Flask, render_template, url_for, flash, redirect, request, abort, session, jsonify, json
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from forms import RegistrationForm, LoginForm

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

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    
    @app.route("/", methods=['GET', 'POST'])
    def index():
        
        return render_template('index.html')
    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = ReusableForm(request.form)
    
        print (form.errors)
        if request.method == 'POST':
            name=request.form['name']
            password=request.form['password']
            email=request.form['email']
            print (name, " ", email, " ", password)
    
        if form.validate():
        # Save the comment here.
            flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')
    
        return render_template('hello2.html', form=form)
@app.route('/browse')
def browse():
    return render_template("browse.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = ReusableForm(request.form)

    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run()