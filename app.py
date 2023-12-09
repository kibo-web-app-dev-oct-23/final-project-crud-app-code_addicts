from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, User, Recipe, Ingredient

# generate random secret using secrets module
import secrets

secret_key = secrets.token_hex(16)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = secret_key
db.init_app(app)


# Index Routes
@app.route("/")
def index():
    return render_template("index.html")


# Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password)

        # Parsing new user into the database
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            flash("Login successful!", "success")

            # Set user id for the session in order to get user details
            session["user_id"] = user.id

            return redirect(url_for("dashboard"))
        else:
            flash("Login unsuccessful. Check email and password.", "danger")
    return render_template("login.html")


# dashboard route
@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        # Get user detail from User table
        user = db.session.get(User, session["user_id"])

        if user:
            # Fetch user's recipes and display on the dashboard
            recipes = Recipe.query.filter_by(user_id=user.id).all()
            return render_template("dashboard.html", user=user, recipes=recipes)
    return redirect(url_for("login"))


# logout route
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out", "info")
    return redirect(url_for("login"))


# recipe management route
@app.route("/recipes")
def recipes():
    recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=recipes)


@app.route("/recipe/<int:recipe_id>")
def view_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    ingredients = Ingredient.query.filter_by(recipe_id=recipe.id).all()
    return render_template("view_recipe.html", recipe=recipe, ingredients=ingredients)


# create recipe route
@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    if "user_id" in session:
        if request.method == "POST":
            title = request.form.get("title")
            ingredients = request.form.get("ingredients")
            instructions = request.form.get("instructions")

            # Create a new recipe object
            user = User.query.get(session["user_id"])
            new_recipe = Recipe(
                title=title,
                ingredients=ingredients,
                instructions=instructions,
                user_id=user.id,
            )
            db.session.add(new_recipe)
            db.session.commit()

            # Split ingredients into a list
            ingredients_list = [
                ingredient.strip() for ingredient in ingredients.split(",")
            ]

            for ingredient in ingredients_list:
                name, quantity = extract_ingredient_data(ingredient)

                new_ingredient = Ingredient(
                    name=name, quantity=quantity, recipe_id=new_recipe.id
                )
                db.session.add(new_ingredient)
            db.session.commit()

            flash("Recipe created successfully!", "success")
            return redirect(url_for("dashboard"))

        return render_template("create_recipe.html")

    return redirect(url_for("login"))


def extract_ingredient_data(ingredient_data):
    parts = ingredient_data.split("-")
    name = parts[0].strip()
    quantity = parts[1].strip() if len(parts) > 1 else None
    return name, quantity


# edit recipe route
@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if "user_id" in session:
        recipe = Recipe.query.get(recipe_id)

        # Check if the logged-in user is the owner of the recipe
        if recipe.user_id == session["user_id"]:
            if request.method == "POST":
                # Update recipe details
                recipe.title = request.form.get("title")
                recipe.ingredients = request.form.get("ingredients")
                recipe.instructions = request.form.get("instructions")

                # Update the recipe in the database
                db.session.commit()

                # Update the ingredients associated with the recipe
                ingredients_list = [
                    ingredient.strip() for ingredient in recipe.ingredients.split(",")
                ]

                # Clear existing ingredients associated with the recipe
                Ingredient.query.filter_by(recipe_id=recipe.id).delete()

                for ingredient in ingredients_list:
                    name, quantity = extract_ingredient_data(ingredient)

                    new_ingredient = Ingredient(
                        name=name, quantity=quantity, recipe_id=recipe.id
                    )
                    db.session.add(new_ingredient)

                db.session.commit()

                flash("Recipe updated successfully!", "success")
                return redirect(url_for("dashboard"))

            return render_template("edit_recipe.html", recipe=recipe)

    return redirect(url_for("login"))


# delete recipe route
@app.route("/delete_recipe/<int:recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    if "user_id" in session:
        recipe = Recipe.query.get(recipe_id)

        # Check if the logged-in user is the owner of the recipe
        if recipe.user_id == session["user_id"]:
            if request.method == "POST":
                # Delete the recipe from the database
                db.session.delete(recipe)

                # Delete associated ingredients
                Ingredient.query.filter_by(recipe_id=recipe.id).delete()

                db.session.commit()

                flash("Recipe deleted successfully!", "success")
                return redirect(url_for("dashboard"))

            return render_template("delete_recipe.html", recipe=recipe)

    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
