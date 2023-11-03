import sqlite3

from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix="/account",
    tags=["Account"]
)


@router.get("/")
@cache(expire=60)
async def get_accounts():
    with sqlite3.connect(database="models/database.db") as connection:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM account;")
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
