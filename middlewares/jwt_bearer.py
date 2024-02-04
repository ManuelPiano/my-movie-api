from fastapi import HTTPException, Request
from utils.jwt_manager import validate_token
from fastapi.security import HTTPBearer

class JwtBearer(HTTPBearer):
     async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['username'] != "admin":
            raise HTTPException(status_code=403, detail="Credenciales inválidas")