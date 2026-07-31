from limits import parse, storage, strategies

from src.config import Settings

from fastapi import HTTPException, status


from functools import wraps

settings = Settings()
store = storage.RedisStorage(settings.redis_url)

limiter = strategies.MovingWindowRateLimiter(store)


window = "minute"
requests = "10 per"

rate_rule = parse(f"{requests} {window}")


def handle_request(user_id: str) -> bool:
    # Check if the user is allowed to proceed
    if limiter.hit(rate_rule, user_id):
        print(f"Request allowed for user {user_id}")
        return True
    else:
        print(f"429 Too Many Requests for user {user_id}")
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
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too Many Requests",
                )

        return wrapper

    return decorator


# *args - def abs(a, b, c, d). tuple = (a, b, c, d)
# **kwargs - def abs(a = 1, b = 2, c = 3, d = 4). dict = {a: 1, b: 2, c: 3, d: 4}

# @ratelimiter(window="1 minute", requests=10)
# @router.get("/users")
# async def all_users() -> list: ...
