import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set JWT secret key
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

# Set token location (common setting to use 'Authorization' header)
app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Token will be in the 'Authorization' header

# Specify the header name where the token will be expected
app.config['JWT_HEADER_NAME'] = 'Authorization'  # This specifies that the JWT will be passed in the Authorization header

# Specify the token type to be used in the header
app.config['JWT_HEADER_TYPE'] = 'Bearer'  # This will prefix the token with 'Bearer' in the Authorization header

# Import routes and token handling
from routes import *


if __name__ == "__main__":
    app.run(debug=True)
