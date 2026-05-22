from flask import Flask, render_template, request, redirect, url_for
from database import init_db, db
from models import Recipe

app = Flask(__name__)
init_db(app)

# Home - list all recipes
@app.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

# Add recipe - show form
@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        instructions = request.form.get('instructions', '').strip()
        cook_time = request.form.get('cook_time', '').strip()
        category = request.form.get('category', '').strip()

        if not title or not ingredients or not instructions:
            return render_template('add.html', error="Please fill in all required fields.")

        new_recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            cook_time=cook_time,
            category=category
        )
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)