# ANSWERS.md

---

## 1. How to Run

Make sure Python 3.8+ is installed. Then:

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

Open http://127.0.0.1:5000 in your browser.
The database file creates itself on first run. No extra setup needed.

---

## 2. Stack Choice

Flask felt like the right size for this — not too much structure,
not too little. SQLite through SQLAlchemy was an easy call since
the data is simple and I didn't need a separate database server.
Tailwind via CDN kept the frontend clean without any build setup.

A worse choice would have been Streamlit. I actually considered
it early on but it's designed for data dashboards, not multi-page
apps with forms and routing. FastAPI would've been overkill too
since I'm just rendering HTML templates, not building a proper API.

---

## 3. One Real Edge Case

In app.py around lines 20-22, before saving a new recipe I check
whether the required fields are actually filled:

```python
if not title or not ingredients or not instructions:
    flash('Please fill in all required fields.', 'error')
    return render_template('add.html')
```

Without this, submitting an empty title would crash the page
because the database column is set to nullable=False. Instead
the user just sees a clean error message and the form stays open.

There's a similar check in the search feature — when splitting
the user's input by commas I filter out empty strings so that
typing only spaces or commas doesn't return weird results.

---

## 4. AI Usage

I used Claude as a reference while building — mostly to clarify
how SQLAlchemy models work and to talk through the project
structure before writing code. Think of it like asking a senior
developer to explain something rather than write it for me.

One thing I changed: the search logic Claude explained used exact
ingredient matching. I changed it to partial matching:

```python
if any(user_ing in recipe_ing for recipe_ing in recipe_ingredients)
```

Exact matching meant searching "egg" wouldn't find recipes with
"eggs" in them which is just annoying in practice. Partial
matching makes the feature actually usable.

---

## 5. Honest Gap

No user accounts. It's a single shared recipe collection right
now which is fine for a personal tool but not for anything
multi-user. I skipped auth intentionally because it would have
eaten most of my time for something that wasn't the core requirement.

With another day I'd add Flask-Login, hash passwords properly,
add a user_id to each recipe, and filter queries by whoever
is logged in. I'd also add recipe image upload — text only
works but a photo makes it feel like a real recipe app.