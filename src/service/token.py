from src.repository.refresh_token import RefreshTokenRepository
from src.service.jwt import JWTPayload, JWTService


class TokenService:
    def __init__(self, jwt_svc: JWTService, refresh_token_repo: RefreshTokenRepository):
        self.jwt_svc = jwt_svc
        self.refresh_token_repo = refresh_token_repo

    def access_token(self, payload: JWTPayload) -> str:
        payload["exp"] = 5
        token = self.jwt_svc.encode_token(payload)

        return token

    def refresh_token(self, payload: JWTPayload) -> str:
        payload["exp"] = 30
        token = self.jwt_svc.encode_token(payload)

        self.refresh_token_repo.save(
            str(payload["sub"]),
            {
                "token": token,
                "user_id": payload["sub"],
                "expires_in": 5000,
            },
        )

        # print(self.refresh_token_repo.get(token))

        return token
