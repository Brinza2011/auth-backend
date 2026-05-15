

from datetime import UTC, datetime, timedelta
from typing import Optional, TypedDict
import jwt


class JWTPayload(TypedDict):
    sub: str
    role: str
    exp: Optional[int]



class JWTService:

    def __init__(self, secret_key: str, algorithm: str = "HS256") -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm


    def encode_token(self, payload: JWTPayload) -> str:
        if not payload["exp"]:
            payload["exp"] = 5


        exp = datetime.now(UTC) + timedelta(minutes=payload["exp"])

        data = {
            "sub": payload["sub"],
            "role": payload["role"],
            "exp": exp
        }

        return jwt.encode(data, self.secret_key, algorithm = "HS256")
    

    def decode_token(self, token: str) -> JWTPayload:
        try:
            decoded_payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return {
                "sub": decoded_payload["sub"],
                "role": decoded_payload["role"],
                "exp": decoded_payload["exp"]
            }
        
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")
        

    def verify_token(self, token: str) -> bool:
        try:
            jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
        
    
