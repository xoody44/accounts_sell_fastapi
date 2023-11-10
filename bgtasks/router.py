from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks

from bgtasks import tasks

router = APIRouter(
    prefix="/buying",
    tags=["Buying"]
)


@router.get("/get_acc")
async def buy_account(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(tasks.send_message, "melnikov2007@list.ru", 1)
        return {
                "status": "access",
                "data": None,
                "detail": None
                }
    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "denied",
                "data": ex,
                "detail": None
            }
        )