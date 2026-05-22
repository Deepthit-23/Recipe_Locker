# 🍳 Recipe Locker

A personal recipe management web app built with Flask and SQLite.
Save, organize, and find recipes based on ingredients you already have.

---

## Features

- Add, view, edit, and delete recipes
- Categorize recipes (Breakfast, Lunch, Dinner, Snack, Dessert)
- Filter recipes by ingredients you have at home
- Data persists between sessions using SQLite
- Clean, responsive UI built with Tailwind CSS

---

## Tech Stack

- **Backend:** Python + Flask
- **Database:** SQLite via SQLAlchemy
- **Frontend:** HTML + Tailwind CSS

---

## How to Run

### Requirements
- Python 3.8 or higher
- pip

### Steps

1. Clone the repository
```bash
git clone https://github.com/Deepthit-23/Recipe_Locker.git
cd recipe-locker
```

2. Create and activate a virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the app
```bash
python app.py
```

5. Open your browser and go to
http://127.0.0.1:5000

That's it. The SQLite database is created automatically on first run.
No configuration needed.

---

## Project Structure
recipe-locker/
├── app.py              # Flask app and all routes
├── models.py           # Recipe database model
├── database.py         # Database setup and connection
├── templates/
│   ├── base.html       # Shared layout and navbar
│   ├── index.html      # Home page - all recipes
│   ├── add.html        # Add new recipe form
│   ├── view.html       # Single recipe view
│   ├── edit.html       # Edit recipe form
│   └── search.html     # Ingredient filter search
├── requirements.txt
├── README.md
└── ANSWERS.md

---

## The Extra Feature — Ingredient Filter

Go to the Search page and type ingredients you have at home
(e.g. `eggs, flour, milk`).

The app finds all recipes that use those ingredients and ranks them
by how many ingredients match. A progress bar shows the match strength.

This solves a real problem — figuring out what you can cook
with what you already have.