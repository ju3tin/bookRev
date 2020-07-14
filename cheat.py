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

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    username = TextField('Userame:', validators=[validators.required()])
    surname = TextField('Surname:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html', error_code='404'), 404
    
    @app.errorhandler(500)
    def special_exception_handler(error):
        return render_template('500.html', error_code='500'), 500


    @app.route("/", methods=['GET', 'POST'])
    def index():
        
        return render_template('index.html')
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = ReusableForm(request.form)
        print (form.errors)
        if request.method == 'POST':
            users = conn[DBS_NAME].users
            username=request.form['username']
            password=request.form['password']
            print (username, " ", password)
            login_user = users.find_one({'username' : username})
          #  login_user = users.find_one({'username' : request.form['username']})


            if login_user:
                if (password) == login_user['password']:
                    session['username'] = request.form['username']
                    return redirect(url_for('browse'))
                    return 'Invalid username/password combination'

        #return 'Invalid username/password combination'

        return render_template("login2.html", form=form)

    @app.route("/questions", methods = ['GET'])
    def questions():
        try:
            
            number = conn[DBS_NAME][COLLECTION_NAME]
            
            
            questions = number.find().sort('_id',pymongo.ASCENDING).limit(1)
            
            return render_template('browseone.html', questions = questions)
        except Exception as e:
            return dumps({'error' : str(e)})

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = ReusableForm(request.form)
    
        print (form.errors)
        if request.method == 'POST':
            users = conn[DBS_NAME].users
            excisting_user = users.find_one({'email' : request.form['email']})
            name=request.form['name']
            surname=request.form['surname']
            username=request.form['username']
            password=request.form['password']
            email=request.form['email']
            print (name, " ", surname, " ", email, " ", password)

            if excisting_user is None:
                
                users.insert({'firstname' : name, 'surname' : surname,'email' : email, 'username' : username, 'password' : password})
                
                
    
        if form.validate():
        # Save the comment here.
            flash('Thanks for registration ' + name)
        else:
            flash('Error: All the form fields are required. ')
    
        return render_template('hello2.html', form=form)
@app.route('/browse')
def browse():
    return render_template("browse.html")

@app.route('/bookdetail')
def bookdetail():
    return render_template("browse1.html")

@app.route("/post/<int:bookID>")
def post(bookID):
    post = conn[DBS_NAME][COLLECTION_NAME].query.get_or_404(bookID)
    return render_template('post.html', title=post.title, post=post)

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