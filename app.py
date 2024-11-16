from flask import Flask
from flask_jwt_extended import JWTManager
from models import init_db
from routes.user_routes import user_routes
from routes.admin_routes import admin_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

# Initialize the database
init_db(app)

# Register routes
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(admin_routes, url_prefix='/admin')

if __name__ == '__main__':
    app.run(debug=True)
