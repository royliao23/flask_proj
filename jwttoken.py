from flask_jwt_extended import create_access_token

def generate_access_token(username):
    """Generate an access token for the given username."""
    return create_access_token(identity=username)
