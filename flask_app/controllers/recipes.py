from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
# from flask_app.models.user import User

# from flask_bcrypt import Bcrypt 
# bcrypt = Bcrypt(app)

@app.route('/create_link')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('recipes_new.html')
    # ,  recipe = Recipe.get_all_recipes()

@app.route('/create_recipe', methods=["POST"])
def new_foods():
    if 'user_id' not in session:
        return redirect('/')
    print(request.form)
    # if recipe fails validation redirect back to create recipe page
    # if not Recipe.validate_recipe(request.form):
    #     print('recipe validate error')
    #     return redirect('/create_link')
    data = {
        # "id" : request.form["id"],
        "r_name": request.form["r_name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "half_hour" : request.form['half_hour'],
        "date_cooked_made" : request.form['date_cooked_made'],
        # the person that is logged in is creating the recipe
        'user_id': session['user_id']
        }
        # entering recipe_id into session to access for view page
    recipe_id = Recipe.create(data)
    session['recipe_id'] = recipe_id
    return redirect('/dash')

@app.route('/dash')
def i_have_been_made():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('dashboard.html')

@app.route('/view_recipe/<int:id>')
def show_me_da_foods(id):
    if 'user_id' not in session:
        return redirect('/')
    # if recipe fails validation redirect back to create recipe page
    # if not Recipe.validate_recipe(request.form):
    #     print('recipe validate error')
    #     return redirect('/create_link')
    user_data = {
        'id': session['user_id']
    }
    data = {
        'id': id
    }

    return render_template('view_recipe.html', current_user = User.get_by_id(user_data), current_recipe = Recipe.get_recipe_by_id(data))
