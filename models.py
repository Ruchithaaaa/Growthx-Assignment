from bson import ObjectId
from flask_pymongo import PyMongo
from datetime import datetime

mongo = PyMongo()

def init_db(app):
    mongo.init_app(app)

# Admin schema
def get_admin_collection():
    return mongo.db.admins

# User schema (for completeness)
def get_user_collection():
    return mongo.db.users

# Assignment schema
def get_assignment_collection():
    return mongo.db.assignments

# Create an admin
def create_admin(username, password):
    admin = {
        "username": username,
        "password": password,  # In a real-world app, you should hash the password
        "createdAt": datetime.utcnow(),
    }
    return get_admin_collection().insert_one(admin)

# Fetch an admin by username
def get_admin_by_username(username):
    return get_admin_collection().find_one({"username": username})

# Fetch all admins
def get_all_admins():
    return list(get_admin_collection().find())

# Create assignment (as before)
def create_assignment(user_id, task, admin_id):
    assignment = {
        "userId": user_id,
        "task": task,
        "admin": admin_id,
        "submittedAt": datetime.utcnow(),
        "status": "pending"
    }
    return get_assignment_collection().insert_one(assignment)

# Fetch assignments for an admin
def get_assignments_for_admin(admin_id):
    return get_assignment_collection().find({"admin": admin_id})

# Accept assignment
def accept_assignment(assignment_id):
    get_assignment_collection().update_one(
        {"_id": ObjectId(assignment_id)},
        {"$set": {"status": "accepted"}}
    )

# Reject assignment
def reject_assignment(assignment_id):
    get_assignment_collection().update_one(
        {"_id": ObjectId(assignment_id)},
        {"$set": {"status": "rejected"}}
    )
