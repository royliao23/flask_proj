from flask import Blueprint, request, jsonify, render_template
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
connectk = os.getenv("connectk")

if not connectk:
    raise ValueError("OpenAI API key is not set. Please set the connectk environment variable.")

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@bp.route('/api/query', methods=['POST'])

def process_query():
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
