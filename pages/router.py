from typing import Annotated

from loguru import logger
import sqlite3

from fastapi import APIRouter, Request, BackgroundTasks, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache
from fastapi.responses import HTMLResponse, RedirectResponse

from bgtasks import tasks

logger.add("logging/logs.log",
           format="{time} {level} {message}",
           level="INFO",
           rotation="100 KB",
           compression="zip")

router_calc = APIRouter(
    prefix="/buying",
    tags=["Buying"]
)
router_account = APIRouter(
    prefix="/account",
    tags=["Account"]
)
router_reviews = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)
router_help = APIRouter(
    prefix="/help",
    tags=["Help"]
)
router_reg = APIRouter(
    prefix="/protect",
    tags=["Authorize"]
)

template = Jinja2Templates(directory="templates")

####################################################
#              router for account page             #
####################################################


@router_account.post("/")
async def template_send(background_tasks: BackgroundTasks, email: Annotated[str, Form()]):
    try:
        logger.info("sending data...")
        background_tasks.add_task(tasks.send_message, email, 1)
        logger.info("message sent")
        return RedirectResponse("/account", status_code=303)
    except Exception as ex:
        logger.error("error while sending message")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "denied",
                "data": ex,
                "detail": None
            }
        )


@router_account.get("/", response_class=HTMLResponse)
async def template_buy(request: Request):
    logger.debug("loading page: Buy account")
    return template.TemplateResponse("buy.html", {"request": request})


@router_account.get("/{account_id}")
@cache(expire=60)
async def get_accounts(account_id):
    logger.debug("loading page: get account by number")
    with sqlite3.connect(database="models/database.db") as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"""
                SELECT * FROM account
                WHERE id = {account_id};
                """)
            result = cursor.fetchall()
            logger.debug(f"connected to the db: {result}")
            return {
                "status": "access",
                "data": result,
                "detail": None
            }
        except Exception as ex:
            logger.error("error while connecting db")
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "data": ex,
                    "detail": None
                }
            )


####################################################
#              router for calc page                #
####################################################


@router_calc.get("/")
async def template_account(request: Request):
    logger.debug("loading page: calc price")
    return template.TemplateResponse("calc.html", {"request": request})


@router_calc.get("/get_acc")
async def buy_account(background_tasks: BackgroundTasks):
    try:
        from bgtasks.tasks import get_email
        background_tasks.add_task(tasks.send_message, get_email(), 1)
        logger.info("message sent")
        return {
            "status": "access",
            "data": None,
            "detail": None
        }
    except Exception as ex:
        logger.error("error while sending message")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "denied",
                "data": ex,
                "detail": None
            }
        )


####################################################
#              router for reviews page             #
####################################################


@router_reviews.get("/")
async def template_reviews(request: Request):
    logger.debug("loading page: reviews")
    return template.TemplateResponse("reviews.html", {"request": request})


####################################################
#              router for help page                #
####################################################


@router_help.get("/")
async def template_help(request: Request):
    logger.debug("loading page: help")
    return template.TemplateResponse("help.html", {"request": request})


####################################################
#              router for register page            #
####################################################

@router_reg.post("/authorize")
async def template_authorize(request: Request):
    logger.debug("loading page: authorize")
    return template.TemplateResponse("form.html", {"request": request})


@router_reg.get("/authorize")
async def template_authorize(request: Request):
    logger.debug("loading page: authorize")
    return template.TemplateResponse("form.html", {"request": request})

# @router_help.get("/jwt/login")
# async def template_registration(request: Request):
#     return template.TemplateResponse("form.html", {"request": request})
