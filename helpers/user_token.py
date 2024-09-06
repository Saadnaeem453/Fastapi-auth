import jwt
from dotenv import load_dotenv
import os


def generate_token(payload: dict):
    jwt_key = "23e23423er23f2f23f23fg23g2g2"
    token= jwt.encode(payload, jwt_key, algorithm="HS256")
    return token

def verify_token(token: str):
    jwt_key = os.getenv("JWT_SECRET_KEY")
    if not jwt_key:
        raise ValueError("JWT_SECRET_KEY environment variable is not set.")
    return jwt.decode(token, jwt_key, algorithms=["HS256"])
