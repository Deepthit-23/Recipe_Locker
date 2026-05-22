markdown# ANSWERS.md

---

## 1. How to Run

Make sure you have Python 3.8+ installed on your machine.

Then run these commands one by one:

```bash
git clone https://github.com/Deepthit-23/Recipe_Locker.git
cd recipe-locker
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Then open your browser and go to http://127.0.0.1:5000

The database creates itself automatically on first run — no setup needed.

---

## 2. Stack Choice

I went with Python and Flask because I wanted something simple
and readable. Flask doesn't force a lot of structure on you —
you can start small and add things as you go, which matched
how I was building this.

For the database I used SQLite through SQLAlchemy. SQLite saves
everything in a single file which is perfect here — no server
to set up, no configuration, and it just works out of the box.
For the frontend I used Tailwind CSS loaded from a CDN so I
didn't have to deal with any build tools.

A worse choice would have been Streamlit. I actually considered
it at first but Streamlit is built for data dashboards, not
for apps with multiple pages and forms. Getting proper routing
and form handling working in Streamlit would have been a fight.
FastAPI would also have been unnecessary here — it's great for
building APIs but since I'm rendering HTML templates directly,
Flask is just cleaner and simpler for this use case.

---

## 3. One Real Edge Case

In app.py on lines 20-22, when a user submits the Add Recipe
form, I check whether the required fields are actually filled
before saving anything:

```python
if not title or not ingredients or not instructions:
    flash('Please fill in all required fields.', 'error')
    return render_template('add.html')
```

Without this check, if someone hits Save with an empty title,
SQLAlchemy would throw an error because the title column is
set to nullable=False in the model. That would crash the page
and show the user a raw server error instead of a helpful message.

With this check, the user just sees a clean red message telling
them what to fix and the form stays open. Same logic exists in
the edit route too.

There's also a second edge case in the search feature. In app.py
when processing search input I do:

```python
search_ingredients = [i.strip().lower() for i in raw_query.split(',') if i.strip()]
```

This handles the case where someone types only spaces or commas
and hits Search. Without the if i.strip() part, we'd end up with
empty strings in the list and the app would match those empty
strings against every recipe, returning wrong results.

---

## 4. AI Usage

I used Claude (claude.ai) throughout this project as a guide
rather than a code writer. Here's an honest breakdown:

- Asked Claude to help plan the project structure and which
  files to create before writing any code.

- Asked Claude to explain how SQLAlchemy models work since
  I hadn't used it much on my own before.

- Asked Claude for the initial version of the ingredient
  filter search logic.

- Asked Claude to help debug a gitignore issue where venv
  was showing up as untracked even after adding it to .gitignore.

One thing I changed from what Claude gave me:

The original search logic Claude suggested used exact matching —
meaning searching "egg" would not find a recipe that had "eggs"
in it. I changed the matching condition from:

```python
if user_ing == recipe_ing
```

to:

```python
if any(user_ing in recipe_ing for recipe_ing in recipe_ingredients)
```

This makes the search use partial matching instead of exact
matching, which is way more useful in practice. Nobody wants
to type the exact spelling of every ingredient to get results.

---

## 5. Honest Gap

The biggest gap in this project is that there are no user
accounts. Right now the app is a single shared recipe collection
— if two people ran it on the same machine they'd see each
other's recipes. I knew this going in and decided not to build
auth because it would have taken most of my time and the core
requirement was persistence and CRUD, not multi-user support.

If I had another day I'd add a simple login system using
Flask-Login with hashed passwords stored in the database.
Each recipe would have a user_id column and queries would
filter by the logged in user so everyone sees only their
own recipes.

I'd also add image upload for recipes. Right now recipes
are text only which works but a photo makes a recipe feel
much more real and usable.