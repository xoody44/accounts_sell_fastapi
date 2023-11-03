from redis import asyncio as aioredis
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from db import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from operations.router import router as router_account
from bgtasks.router import router as router_buying

app = FastAPI(
    title="troll"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(router_account)

app.include_router(router_buying)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    try:
        return f"Hello, {user.email}"
    except Exception as ex:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "data": "Hello, friend! pls authorize",
                "detail": "Unauthorized",
            }

        )


@app.get("/unprotected-route")
def unprotected_route():
    return "Hello, friend! pls authorize"


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
