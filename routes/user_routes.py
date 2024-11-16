from flask import Blueprint, request, jsonify
from models import create_assignment, get_admin_by_username, get_all_admins, get_user_collection
from utils.validators import validate_user_input
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()

    # Validate input data (check for missing username or password)
    validation_error = validate_user_input(data)
    if validation_error:
        return validation_error
    
    # Check if the user already exists
    existing_user = get_user_collection().find_one({"username": data["username"]})
    
    if existing_user:
        return jsonify({"error": "User with this username already exists"}), 400

    # If the data is valid then create new user
    user = {
        "username": data["username"],
        "password": data["password"]  # In production, hash the password before saving
    }

    # Insert the new user into the database
    get_user_collection().insert_one(user)

    return jsonify({
        "message": "User registered successfully!",
    }), 201

@user_routes.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = get_user_collection().find_one({"username": data["username"]})
    
    if not user or user["password"] != data["password"]:
        return jsonify({"error": "Invalid username or password"}), 401

    token = create_access_token(identity=data["username"])
    return jsonify({"message": "Login successful", "access_token": token}), 200


@user_routes.route('/upload', methods=['POST'])
@jwt_required()
def upload_assignment():
    data = request.get_json()
    user_id = data.get("userId")
    task = data.get("task")
    admin_id = data.get("admin")
    
    current_user = get_jwt_identity()
    # Check if current logged in user is trying to upload the assignment
    if current_user != user_id:
        return jsonify({"error": "Authentication failed"})
    
    # Check if the assignment is being assigned is valid
    if not get_admin_by_username(admin_id):
        return jsonify({"error": "Not a valid admin"}), 400

    # Check if data is valid
    if not user_id or not task or not admin_id:
        return jsonify({"error": "Missing required fields"}), 400
    
    create_assignment(user_id, task, admin_id)
    return jsonify({"message": "Assignment uploaded successfully!"}), 201

# Get All Admins (Requires Authentication)
@user_routes.route('/admins', methods=['GET'])
# Show list of all admins(only usernames)
def list_admins():
    admins = get_all_admins()
    admin_list = [{"username": admin["username"]} for admin in admins]
    
    return jsonify(admin_list), 200
