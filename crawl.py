from flask import Flask
from src.routes import crawler_routes

app = Flask(__name__)

app.register_blueprint(crawler_routes)

if __name__ == "__main__":
    app.run(debug=True)
