from fastapi import APIRouter, Response, Request
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from models.user_model import User
from helpers.user_token import generate_token

router = APIRouter()
ph = PasswordHasher()

class SignupPayload(BaseModel):
    name: str
    email: str
    password: str

class LoginPayload(BaseModel):
    email: str
    password: str

class LogoutPayload(BaseModel):
    token: str

@router.post("/signup")
async def user_signup(data: SignupPayload):
    if await User.filter(email=data.email).first():
        raise HTTPException(
            status_code=400,
            detail="You are already registered"
        )
    hashed_password = ph.hash(data.password)
    user = User(
        name=data.name,
        email=data.email,
        password=hashed_password
    )
    await user.save()
    return {'Detail': "Registered Successfully"}

@router.post("/login")
async def login_user(data: LoginPayload, response: Response):
    user = await User.filter(email=data.email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Invalid Credentials"
        )

    try:
        ph.verify(user.password, data.password)
        
        token = generate_token({"id": user.id})
        response.set_cookie("authToken" , token)
        return {"success": True, "Token": token}
    
    except VerifyMismatchError:
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"{str(e)}"
        )

@router.post("/logout")
async def logout_user(request: Request, response: Response):
    token = request.cookies.get("authToken")
    if not token:
        raise HTTPException(
            status_code=400,
            detail="Not Logged In"
        )
    response.delete_cookie("authToken")
    return {"detail": "Logged out successfully"}
