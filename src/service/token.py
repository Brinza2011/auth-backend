from src.service.jwt import JWTPayload, JWTService


class TokenService:
    def __init__(self, jwt_svc: JWTService):
        self.jwt_svc = jwt_svc


    def access_token(self, payload: JWTPayload) -> str:
        payload["exp"] = 5
        token = self.jwt_svc.encode_token(payload)

        return token


    def refresh_token(self, payload: JWTPayload) -> str:
        payload["exp"] = 30
        token = self.jwt_svc.encode_token(payload)

        return token  