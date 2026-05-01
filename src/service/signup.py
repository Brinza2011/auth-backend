from src.repository.user import UserRepository


class SignupService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo
