import sentry_sdk
from loguru import logger
from redis import asyncio as aioredis
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from auth.auth import auth_backend
from config import REDIS_HOST, APP_PORT, APP_HOST
from db import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from pages.router import router_account, router_calc, router_reviews, router_help, router_reg

app = FastAPI(
    title="troll"
)

sentry_sdk.init(
    dsn="https://912c3b8c168a72d090b48deba5a44d51@o4506394449739776.ingest.sentry.io/4506394452754432",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

logger.add("logging/logs.log",
           format="{time} {level} {message}",
           level="INFO",
           rotation="100 KB",
           compression="zip")

origins = [
    f"http://{APP_HOST}:{APP_PORT}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.debug(f"middleware is working...\n{response}")
    return response


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
app.include_router(router_calc)
app.include_router(router_reviews)
app.include_router(router_help)
app.include_router(router_reg)

app.mount("/static", StaticFiles(directory="static"), name="static")

template = Jinja2Templates(directory="templates")


@app.get("/")
async def main(request: Request):
    logger.info("main page")
    return template.TemplateResponse("index.html", {"request": request})


@app.get("/protected-route")
async def protected_route(user: User = Depends(current_user)):
    try:
        logger.info("protected-route")
        return f"Hello, {user.email}"
    except Exception as ex:
        logger.error("""
                    "status": "error",
                    "data": "Hello, friend! pls authorize",
                    "detail": "Unauthorized"
                    """)
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "data": ex,
                "detail": "Unauthorized",
            }

        )


@app.get("/unprotected-route")
async def unprotected_route():
    logger.info("unprotected-route")
    return "Hello, friend! pls authorize"


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logger.info("redis is working...")


if __name__ == "__main__":
    uvicorn.run("main:app")
