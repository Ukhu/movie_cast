from flask import Flask
from flask_cors import CORS
from models import setup_db

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    @app.route('/')
    def welcome():
        return 'Welcome to the MovieCast API'

    return app

app = create_app()

if __name__ == '__main__':
    app.run()