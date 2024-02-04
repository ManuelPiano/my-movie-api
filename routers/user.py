from fastapi.responses import JSONResponse
from fastapi import APIRouter
from pydantic import BaseModel
from utils.jwt_manager import create_token

user_router = APIRouter()
class user(BaseModel):
    username: str
    password: str

@user_router.post('/login', tags=['auth'])
def login(user: user):
     if user.username == "admin" and user.password == "admin":
         token: str = create_token(user.dict())
         return JSONResponse(status_code=200, content=token)
