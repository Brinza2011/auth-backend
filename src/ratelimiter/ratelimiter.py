from functools import wraps
from fastapi import HTTPException, Request, status
from limits import parse, storage, strategies
from src.config.settings import Settings


settings = Settings()

store = storage.RedisStorage(settings.redis_url)

limiter = strategies.MovingWindowRateLimiter(store)

window = "minute"
requests = "10 per"

rate_rule = parse(f"{requests} {window}")

def handle_request(user_id: str) -> bool:
    if limiter.hit(rate_rule, user_id):
        print(f"Request allowed for user {user_id}")
        return True
    else:
        print(f"429 Too many requests for user {user_id}")
        return False
    

def rate_limiter(window: str, requests: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = kwargs.get("user_id")
            if handle_request(user_id):
                return await func(*args, **kwargs)
            else:
                raise HTTPException(
                    status_code = status.HTTP_429_TOO_MANY_REQUESTS,
                    detail = "Too many requests"
                )
        return wrapper
    return decorator


# @ratelimiter(window = "1 minute", request = 10)
# @router.get("/users")
# async def all_users() -> :



class RateLimiter:
    def __init__(self, window: str, limit: int):
        self.window = window
        self.limit = limit
        self.rate_rule = parse(f"{limit} per {window}")

    async def __call__(self, request: Request):
        user_id = request.headers.get("user_id")

        if limiter.hit(self.rate_rule, user_id):
            stats = limiter.get_window_stats(
                self.rate_rule,
                user_id,
            )

            n = self.limit - stats.remaining

            print(
                f"user_id={user_id} "
                f"сделал {n} запросов в {self.window}"
            )
            return

        raise HTTPException(
            status_code=429,
            detail="Too many requests",
        )

