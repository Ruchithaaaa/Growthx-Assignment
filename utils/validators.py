from flask import jsonify

def validate_user_input(data):
    # Check if the user input is null
    if len(data["username"])<=0:
        return jsonify({"error": "Username cannot be null"}), 400
    # Check if the user and password field exits in the JSON object
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Missing required fields: username and password"}), 400
    # Password validation to check if it is above or equal to 6 characters in length
    if len(data["password"]) < 6:
        return jsonify({"error": "Password must be at least 6 characters long"}), 400
    return None
