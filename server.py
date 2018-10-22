from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
from helper import authorize_admin
from model import Dog, Prospect, DogPhoto, GenPhoto, connect_to_db, db
import os

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET']
GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']


@app.route('/', methods=['GET', 'POST'])
def index():
    """Homepage"""

    return render_template("index.html", google_client_id=GOOGLE_CLIENT_ID)


@app.route('/about')
def about():
    """Display the About page"""

    return render_template("about.html")


@app.route('/parents')
def parents():
    """Display the Parents page"""

    return render_template("parents.html")


@app.route('/contact')
def contact():
    """Display the Parents page"""

    return render_template("contact.html")


@app.route('/pup/<id>')
def display_pup(id):
    """Display the Parents page"""

    return render_template("contact.html")


@app.route('/admin')
def display_admin_page():
    """Display the Parents page"""

        # execute this if the user submitted the login form
    if request.args:
        email = request.args.get('email')
        password = request.args.get('password')

        if authorize_admin(email, password):
                session['authorized'] = True
                return redirect('/admin-home')
        else:
            flash("Username and password do not match")


    return render_template("admin.html")


@app.route('/admin-home', methods=['GET', 'POST'])
def display_admin_home_page():
    """Display the Parents page"""

    if session['authorized']:
        return render_template("admin-home.html")

    else:
        return render_template('home.html')


@app.route('/add-dog', methods=['POST'])
def add_dog():

    status = False

    name = request.args.get('name')
    sex = request.args.get('sex')
    availability = request.args.get('availability')
    description = request.args.get('description')

    if availability == "Available":
        status = True

    new_dog = Dog(name=name, sex=sex, status=status, description=description)
    
    db.session.add(new_dog)
    db.session.commit()

    return redirect("admin-home.html")


if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug


    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(port=9810, host='0.0.0.0')