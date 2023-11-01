from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend, BearerTransport

cookie_transport = CookieTransport(cookie_max_age=3600, cookie_name="trolls")

SECRET = "fsgud9hiynb9suginhfodybuhsgnio9fbdyigynofdbg9ioyndbfsg9iyondbpfigoyndfyg9iondfyigsondf9iygondf9igsydnobf"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
