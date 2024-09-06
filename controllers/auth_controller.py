from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel , EmailStr
from argon2 import PasswordHasher
from models.user_model import User

router = APIRouter
ph = PasswordHasher()


class SignupPayload(BaseModel):
      name:str
      email:EmailStr
      password:str

class LoginPayload(BaseModel):
      email:EmailStr
      password:str
class LogoutPayload(BaseModel):
      token:str

@router.post("/signup")
async def user_signup(data:SignupPayload):
      if await User.filter(email= data.email).first():
            raise HTTPException(
                  status_code=400,
                  detail="You are already registered"
            )
      hashedPassword= ph.hash(data.password)
      user = User(
            name=data.name,
            email=data.email,
            password=data.password
      )
      await user.save()
      return {'Detail' : "Registered Successfully"}

