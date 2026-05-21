from flask import Flask
from database import init_db

app = Flask(__name__)
init_db(app)

@app.route('/')
def home():
    return 'Recipe Locker is running!'

if __name__ == '__main__':
    app.run(debug=True)