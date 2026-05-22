from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, db
from models import Recipe
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
init_db(app)

# Home - list all recipes
@app.route('/')
def home():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

# Add recipe
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
            flash('Please fill in all required fields.', 'error')
            return render_template('add.html')

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
        flash('Recipe saved successfully!', 'success')
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
            flash('Please fill in all required fields.', 'error')
            return render_template('edit.html', recipe=recipe)

        recipe.title = title
        recipe.description = request.form.get('description', '').strip()
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        recipe.cook_time = request.form.get('cook_time', '').strip()
        recipe.category = request.form.get('category', '').strip()

        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('view_recipe', id=recipe.id))

    return render_template('edit.html', recipe=recipe)

# Delete recipe
@app.route('/delete/<int:id>')
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted.', 'success')
    return redirect(url_for('home'))

# Ingredient search
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        raw_query = request.form.get('ingredients', '').strip()

        if not raw_query:
            return render_template('search.html', searched=True, results=[], query='')

        search_ingredients = [i.strip().lower() for i in raw_query.split(',') if i.strip()]

        if not search_ingredients:
            return render_template('search.html', searched=True, results=[], query='')

        all_recipes = Recipe.query.all()
        results = []

        for recipe in all_recipes:
            recipe_ingredients = [i.strip().lower() for i in recipe.ingredients.split(',') if i.strip()]

            match_count = sum(
                1 for user_ing in search_ingredients
                if any(user_ing in recipe_ing for recipe_ing in recipe_ingredients)
            )

            if match_count > 0:
                results.append((recipe, match_count, len(search_ingredients)))

        results.sort(key=lambda x: x[1], reverse=True)

        return render_template('search.html', searched=True, results=results, query=raw_query)

    return render_template('search.html', searched=False, results=[], query='')

if __name__ == '__main__':
    app.run(debug=True)