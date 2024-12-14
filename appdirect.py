import os
from flask import Flask, request, jsonify,render_template
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

#set JWT_SECRET_KEY
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY") 
bcrypt = Bcrypt(app)
jwt = JWTManager(app)



# Set your OpenAI API key
connectk = os.getenv("connectk")

# Dummy user database
users = {"testuser": bcrypt.generate_password_hash("password").decode('utf-8')}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# User login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users and bcrypt.check_password_hash(users[username], password):
        access_token = create_access_token(identity=username)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"msg": "Invalid credentials"}), 401

# User login endpoint
@app.route('/openai', methods=['POST'])
# @jwt_required()
def get_answer():
    data = request.get_json()
    user_query = data.get('query')
    
    if not user_query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        # Define the prompt template
        prompt = PromptTemplate.from_template(user_query)

        # Create the ChatOpenAI instance
        chat_model = ChatOpenAI(connectk=connectk, model="gpt-4")

        # Combine prompt and model to create a runnable sequence
        # In the new API, use prompt | chat_model instead of LLMChain
        response = (prompt | chat_model).invoke({})

        # Output the response
        print(response)
        return jsonify({"resp":response.content})
    
    
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500  # Catch any other exceptions


# Protected data endpoint
@app.route('/data', methods=['GET'])
@jwt_required()
def get_data():
    current_user = get_jwt_identity()
    return jsonify({"data": f"This is protected data for {current_user}."}), 200

if __name__ == "__main__":
    app.run(debug=True)
