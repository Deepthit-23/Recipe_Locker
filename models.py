from database import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    cook_time = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Recipe {self.title}>'