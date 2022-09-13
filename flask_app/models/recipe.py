from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user

# from flask_bcrypt import Bcrypt        
# bcrypt = Bcrypt(app)

from flask import flash

class Recipe:
    # could enter variable here and set it = to schema name in workbench
    def __init__( self , data ):
        self.id = data['id']
        self.maker = None
        self.r_name = data['r_name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.half_hour = data['half_hour']
        self.date_cooked_made = data['date_cooked_made']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        

    # class method to save our recipe to the database
    # KEEP EDITING THIS TO MATCH REQUEST FORM
    @classmethod
    def create(cls, data ):
        query = "INSERT INTO recipes ( r_name, description, instructions, date_cooked_made ,half_hour, user_id, created_at, updated_at ) VALUES ( %(r_name)s , %(description)s, %(instructions)s, %(date_cooked_made)s, %(half_hour)s, %(user_id)s, NOW(), NOW() );"
        results = connectToMySQL('recipes_users_schema').query_db( query, data )
        # prints id of recipe
        print(results)
        return results

    @staticmethod
    def validate_recipe( recipe ):
        is_valid = True
        # first_name and last name must be longer than 2 characters
        if len(recipe['r_name']) < 3:
            flash("Recipe name must be at least 3 characters.")
            print('recipe name flash')
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.")
            print('description flash')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be longer.")
            print('instructions flash')
            is_valid = False
            return is_valid

    @classmethod
    # if no data is passed to the classmethod then you do not need it in the query results
    def get_all_with_maker(cls):
        # put the many on the left hand side of the join so visually it makes more sense
        query = "SELECT * from recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL('recipes_users_schema').query_db( query)
        all_recipes = []
        for row in results:
            # creating recipe instance here
            one_recipe = cls(row)
            user_data = {
                "id" :row['users.id'],
                "first_name" :row['first_name'],
                "last_name" :row['last_name'],
                # using none here removes access to password at final end point
                "password" :None,
                "email" :row['email'],
                # again you can use none here if this info is irrelevant at end point
                # this is causing a key error with (users.created_at) / doesnt like 'created_at' either
                "updated_at" :None,
                "created_at" :None,
                
            }
            # model.class.variable for dictionary above
            user_obj = user.User(user_data)
            # the recipes maker attribute is being filled in with user object created above
            one_recipe.maker = user_obj
            # adding single recipe into list of recipes. adding recipe instance that contains a users instance in it.
            all_recipes.append(one_recipe)
        return all_recipes
        
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes_users_schema').query_db(query)
        recipes = []
        for one_recipe in results:
            recipes.append( cls(one_recipe) )
        print(recipes)
        return recipes
    
    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes_users_schema').query_db(query,data)
        print(results)
        one_recipe = cls(results[0])
        one_recipe_maker_info = {
            "id": results[0]['users.id'],
            "created_at": None,
            "first_name": results[0]['first_name'],
            "last_name" : results[0]['last_name'],
            "email" : results[0]['email'],
            "updated_at": None,
            "password": None,
            "instructions": results[0]['instructions'],
            "date_cooked_made": results[0]['date_cooked_made'],
            "half_hour": results[0]['half_hour'],
            "r_name": results[0]['r_name']
        }
        author = user.User(one_recipe_maker_info)
        one_recipe.maker = author
        return one_recipe