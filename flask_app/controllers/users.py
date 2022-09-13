from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('registration.html', user = User.get_all_users())

@app.route('/create_user', methods=["POST"])
def create_user():
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "id" : request.form["id"],
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
        }
    user_id = User.save(data)
    # user__id for the result of am insert query
    session['user_id'] = user_id
    # Redirect after saving to the database.
    return redirect('/dash')

@app.route('/dash')
def i_exist_yo():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    # passing data in below on user.get_by_id passes the data over to the model file
    return render_template('dashboard.html', current_user = User.get_by_id(data), all_the_recipes = Recipe.get_all_with_maker())

# LOGIN AUTHENTICATION 
# email must already exist in database
# password must match hased password in the database for the existing user
@app.route('/login', methods = ['POST'])
def login():
    # show me what you got!
    print(request.form)
    # see if the email provided exists in the database via a data dict
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # email is not registered in the db
    if not user_in_db:
        # security! say both are wrong so that the hacker doesnt know what they got wrong
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password. security! say both are wrong so that the hacker doesnt know what they got wrong
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session. Correct email has been entered, correct password has been entered, and both email and password are on the same row in the database
    session['user_id'] = user_in_db.id
    # user_in_db.id dot notation for the result of a select query
    return redirect("/dash")

@app.route('/logout')
def logout():
    session.clear()
    # passing data in below on user.get_by_id passes the data over to the model file
    return redirect('/')