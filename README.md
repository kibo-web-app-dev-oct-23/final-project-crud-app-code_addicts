Flask application for a recipe management system.

Here's a summary of its functionality:

1.User Authentication:

    Users can register for an account ('/register') by providing a username, email, and password.

    Users can log in ('/login') using their email and password, with password hashing for security.

    User sessions are managed, allowing access to certain routes only when logged in.
2.Dashboard:

    Authenticated users can view a personalized dashboard ('/dashboard') that displays their recipes.

    The dashboard lists the user's recipes and provides links to view, edit, and delete each recipe.
3.Recipe Management:

    Authenticated users can view a list of all recipes ('/recipes').

    Users can view the details of a specific recipe ('/recipe/<int:recipe_id>').

    Users can create a new recipe ('/create_recipe') by providing a title, ingredients, and instructions.
4.Recipe Editing:

    Authenticated users can edit their own recipes by navigating to the "Edit" link on the dashboard.

    A separate route ('/edit_recipe/<int:recipe_id>') handles the editing of recipe details.
5.Recipe Deletion:

    Authenticated users can delete their own recipes by navigating to the "Delete" link on the dashboard.

    A separate route ('/delete_recipe/<int:recipe_id>') handles the deletion of recipes with a confirmation step.
6.Logout:

    Users can log out ('/logout'), ending their session.
7.Recipe and Ingredient Models:

    The application uses SQLAlchemy to define models for users, recipes, and ingredients, with relationships between them.
Database Setup:

    The application creates SQLite databases ('site.db') and tables for users, recipes, and ingredients.
Styling and Flash Messages:

    Basic styling is applied to the HTML templates.

    Flash messages are used to provide feedback to users on actions such as account creation, login, and recipe management.
 
    
This application provides a simple web interface for users to manage their recipes, including creating, editing, and deleting recipes. The routes and templates are organized to facilitate user interaction with the system.


For our Schema:
1. User Model:

    a.Represents a user in the system.

    b.Fields:

       'id': Auto-incremented unique identifier.

        'username': User's username, must be unique.

        'email': User's email, must be unique.

        'password_hash': Hashed password for security.

    c.Defines a one-to-many relationship with the Recipe model. A user can have multiple recipes.

Recipe Model:

    a.Represents a recipe in the system.

    b.Fields:
        'id': Auto-incremented unique identifier.

       ' title': Title of the recipe.

        'ingredients': Ingredients of the recipe (stored as a text field).

        'instructions': Instructions for preparing the recipe.

        'date_created': Date and time when the recipe was created.

        'user_id': Foreign key referencing the id field in the User model.

    c.Defines a one-to-many relationship with the Ingredient model. A recipe can have multiple ingredients.

Ingredient Model:

    a.Represents an ingredient in the system.

    b.Fields:
        'id': Auto-incremented unique identifier.

        'name'': Name of the ingredient.

        'quantity': Quantity of the ingredient (optional).

        'recipe_id': Foreign key referencing the id field in the Recipe model.


This schema defines the structure of the database tables ('User', 'Recipe', and 'Ingredient') and the relationships between them. It allows you to store information about users, their recipes, and the ingredients associated with each recipe.

