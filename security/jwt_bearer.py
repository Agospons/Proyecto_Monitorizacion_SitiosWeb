from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from security.jwt_manager import create_token
import jwt 
from jose import JWTError

SECRET_KEY = "clave_secreta"
ALGORITHM = "HS256"


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Esquema de autenticación inválido")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token inválido o expirado")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Credenciales no encontradas")

    def verify_jwt(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return True
        except JWTError as e:
            print("❌ JWT Error:", e)
            return False