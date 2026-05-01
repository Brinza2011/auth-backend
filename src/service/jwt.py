from typing import TypedDict

import jwt

# Encoding a token
secret = "your-256-bit-secret"
payload = {"user_id": 123, "role": "admin"}
token = jwt.encode(payload, secret, algorithm="HS256")

# Decoding and verifying
try:
    decoded_payload = jwt.decode(token, secret, algorithms=["HS256"])
    print(decoded_payload)
except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidTokenError:
    print("Invalid token")


class JWTPayload(TypedDict):
    user_id: int
    role: str


class JWTService:
    def __init__(self, secret_key: str, algorithm: str = "HS256") -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm

    def encode_token(self, payload: JWTPayload) -> str:
        data = {"user_id": payload["user_id"], "role": payload["role"]}

        return jwt.encode(data, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> JWTPayload:
        try:
            decoded_payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            return {
                "user_id": decoded_payload["user_id"],
                "role": decoded_payload["role"],
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
