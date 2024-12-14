import os
from flask import request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from app import app

bcrypt = Bcrypt(app)

# Dummy user database (should replace with a real database)
users = {"testuser": bcrypt.generate_password_hash("password").decode('utf-8')}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """User login endpoint."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users and bcrypt.check_password_hash(users[username], password):
        from jwttoken import generate_access_token
        access_token = generate_access_token(username)
        return jsonify({"access_token": access_token}), 200
    
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/openai', methods=['POST']) 
def get_answer():
    """Get a response from OpenAI based on a user query."""
    data = request.get_json()
    user_query = data.get('query')
    
    if not user_query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        # Define the prompt template
        from langchain_openai import ChatOpenAI
        from langchain.prompts import PromptTemplate

        prompt = PromptTemplate.from_template(user_query)
        chat_model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4")

        response = (prompt | chat_model).invoke({})
        return jsonify({"resp": response.content})
    
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    """Protected endpoint for authenticated users."""
    current_user = get_jwt_identity()
    return jsonify({"data": f"This is protected data for {current_user}."}), 200
