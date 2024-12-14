steps to run the app:
1. clone from github:https://github.com/royliao23/flask_proj.git
2. create .env file under project root as: 
    JWT_SECRET_KEY=.....
    OPENAI_API_KEY=.....
3. create a virtual enviroment under project root: python -m venv flaskenv
4. activate env like command:. flaskenv/scripts/activate
5. install dependant libs under project root: pip install -r requirements.txt
6. start app under project root option1:flask run 
7. optional  -> start app under project root option:python app.py
8. open the browser and check if it works

Features:
1. jwt is not needed to AI Query System. just url:http://127.0.0.1:5000/
2. http://127.0.0.1:5000/data is a secure endpoint, it needs jwt token which can be generated after login with hardcoded user. With token available and send with header, it works. I tested this in Postman
