import os

class Config:
    SECRET_KEY = os.urandom(24)
    MONGO_URI = "mongodb://localhost:27017/assignment_portal"
    JWT_SECRET_KEY = os.urandom(24)