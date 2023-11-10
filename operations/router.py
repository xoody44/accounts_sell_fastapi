import sqlite3

from fastapi import APIRouter, HTTPException, Request
from fastapi_cache.decorator import cache
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/account",
    tags=["Account"]
)

template = Jinja2Templates(directory="templates")


@router.get("/")
async def main(request: Request):
    return template.TemplateResponse("buy.html", {"request": request})


@router.get("/{account_id}")
@cache(expire=60)
async def get_accounts(account_id):
    with sqlite3.connect(database="models/database.db") as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                f"""
                SELECT * FROM account
                WHERE id = {account_id};
                """)
            result = cursor.fetchall()
            return {
                    "status": "access",
                    "data": result,
                    "detail": None
                }
        except Exception as ex:
            raise HTTPException(
                status_code=500,
                detail={
                    "status": "error",
                    "data": ex,
                    "detail": None
                }
            )
