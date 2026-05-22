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
# View single recipe
@app.route('/recipe/<int:id>')
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return render_template('view.html', recipe=recipe)

# Edit recipe
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        instructions = request.form.get('instructions', '').strip()

        if not title or not ingredients or not instructions:
            return render_template('edit.html', recipe=recipe, error="Please fill in all required fields.")

        recipe.title = title
        recipe.description = request.form.get('description', '').strip()
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        recipe.cook_time = request.form.get('cook_time', '').strip()
        recipe.category = request.form.get('category', '').strip()

        db.session.commit()
        return redirect(url_for('view_recipe', id=recipe.id))

    return render_template('edit.html', recipe=recipe)

# Delete recipe
@app.route('/delete/<int:id>')
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)