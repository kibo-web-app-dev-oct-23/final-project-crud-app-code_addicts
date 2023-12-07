from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, User, Recipe, Ingredient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

# Routes

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        Flask('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            Flask('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            Flask('Login unsuccessful. Check email and password.', 'danger')
    return render_template('login.html')

#dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        # Fetch user's recipes and display on the dashboard
        recipes = Recipe.query.filter_by(user_id=user.id).all()
        return render_template('dashboard.html', user=user, recipes=recipes)
    return redirect(url_for('login'))

#logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    Flask('You have been logged out', 'info')
    return redirect(url_for('login'))

#recipe management route
@app.route('/recipes')
def recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    ingredients = Ingredient.query.filter_by(recipe_id=recipe.id).all()
    return render_template('view_recipe.html', recipe=recipe, ingredients=ingredients)

# create recipe route
@app.route('/create_recipe', methods=['GET', 'POST'])
def create_recipe():
    if 'user_id' in session:
        if request.method == 'POST':
            title = request.form.get('title')
            ingredients = request.form.get('ingredients')
            instructions = request.form.get('instructions')

            # Split ingredients into a list
            ingredients_list = [ingredient.strip() for ingredient in ingredients.split(',')]

            # Create a new recipe
            user = User.query.get(session['user_id'])
            new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, user_id=user.id)
            db.session.add(new_recipe)
            db.session.commit()

            # Associate ingredients with the recipe
            for ingredient in ingredients_list:
                ingredient_data = ingredient.split('-')
                name = ingredient_data[0].strip()
                quantity = ingredient_data[1].strip() if len(ingredient_data) > 1 else None
                unit = ingredient_data[2].strip() if len(ingredient_data) > 2 else None
                new_ingredient = Ingredient(name=name, quantity=quantity, unit=unit, recipe_id=new_recipe.id)
                db.session.add(new_ingredient)
            db.session.commit()

            Flask('Recipe created successfully!', 'success')
            return redirect(url_for('dashboard'))

        return render_template('create_recipe.html')

    return redirect(url_for('login'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

