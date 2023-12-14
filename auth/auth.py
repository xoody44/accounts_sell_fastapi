from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

from config import SECRET_KEY

cookie_transport = CookieTransport(cookie_max_age=3600, cookie_name="trolls")

SECRET = SECRET_KEY


async def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
