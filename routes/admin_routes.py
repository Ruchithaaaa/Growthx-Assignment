from bson import ObjectId
from flask import Blueprint, request, jsonify
from models import accept_assignment, create_admin, get_admin_by_username, get_all_admins, get_assignment_collection, get_assignments_for_admin, reject_assignment
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.validators import validate_user_input

admin_routes = Blueprint('admin_routes', __name__)

# Admin Registration
@admin_routes.route('/register', methods=['POST'])
def register_admin():
    data = request.get_json()
    
    # Validate input (same as user validation)
    validation_error = validate_user_input(data)
    if validation_error:
        return validation_error

    # Check if the admin already exists
    existing_admin = get_admin_by_username(data["username"])
    if existing_admin:
        return jsonify({"error": "Admin with this username already exists"}), 400

    # Create new admin
    create_admin(data["username"], data["password"])
    
    return jsonify({"message": "Admin registered successfully!"}), 201

# Admin Login
@admin_routes.route('/login', methods=['POST'])
def login_admin():
    data = request.get_json()
    
    # Check if the admin exists
    admin = get_admin_by_username(data["username"])
    if not admin or admin["password"] != data["password"]:
        return jsonify({"error": "Invalid username or password"}), 401

    # Create access token
    token = create_access_token(identity=data["username"])
    
    return jsonify({"message": "Login successful", "access_token": token}), 200

# Route to view assignments assigned to the admin
@admin_routes.route('/assignments', methods=['GET'])
@jwt_required()
def get_assignments():
    """
    This route returns all assignments that are tagged to the currently authenticated admin.
    """
    # Get the current admin username (identity from JWT)
    current_admin = get_jwt_identity()

    # Fetch assignments tagged to the current admin and that are still pending
    assignments_cursor = get_assignments_for_admin(current_admin)

    # Convert the cursor to a list and return as JSON response
    assignments = []
    # Show all assignemnts
    for assignment in assignments_cursor:
        assignments.append({
            "assignmentId": str(assignment["_id"]),  # Convert ObjectId to string
            "userId": assignment["userId"],
            "task": assignment["task"],
            "submittedAt": assignment["submittedAt"].strftime("%Y-%m-%d %H:%M:%S"),  # Format date
            "status": assignment["status"]
        })

    # If you need to display only pending assignemnts uncomment this and add condition in get_assignments_for_admin
    # if not assignments:
    #     return jsonify({"message": "No pending assignments found"}), 404

    return jsonify(assignments), 200

# Accept an assignment
@admin_routes.route('/assignments/<string:assignment_id>/accept', methods=['POST'])
@jwt_required()
def accept_assignment_route(assignment_id):
    """
    This route allows an admin to accept an assignment.
    """
    # Get the current admin's identity (username) from the JWT token
    current_admin = get_jwt_identity()

    # Fetch the assignment from the database
    assignment = get_assignment_collection().find_one({"_id": ObjectId(assignment_id), "admin": current_admin})

    # Check if assignment exists
    if not assignment:
        return jsonify({"error": "Assignment not found or you are not authorized to accept this assignment"}), 404

    # If the assignment is already accepted or rejected, return an error
    if assignment["status"] in ["accepted", "rejected"]:
        return jsonify({"error": "Assignment already processed"}), 400

    # Accept the assignment
    accept_assignment(assignment_id)

    return jsonify({"message": "Assignment accepted successfully"}), 200


# Reject an assignment
@admin_routes.route('/assignments/<string:assignment_id>/reject', methods=['POST'])
@jwt_required()
def reject_assignment_route(assignment_id):
    """
    This route allows an admin to reject an assignment.
    """
    # Get the current admin's identity (username) from the JWT token
    current_admin = get_jwt_identity()

    # Fetch the assignment from the database
    assignment = get_assignment_collection().find_one({"_id": ObjectId(assignment_id), "admin": current_admin})

    # Check if assignment exists
    if not assignment:
        return jsonify({"error": "Assignment not found or you are not authorized to reject this assignment"}), 404

    # If the assignment is already accepted or rejected, return an error
    if assignment["status"] in ["accepted", "rejected"]:
        return jsonify({"error": "Assignment already processed"}), 400

    # Reject the assignment
    reject_assignment(assignment_id)

    return jsonify({"message": "Assignment rejected successfully"}), 200
