from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from database import Base, engine, get_db
from schemas import SmartHomeRequest
from services import create_plan, get_all_plans, get_plan_by_id

Base.metadata.create_all(bind=engine)

app = FastAPI()

def success(status_code, message, data, request: Request):
    return {
        "statusCode": status_code,
        "message": message,
        "error": None,
        "data": data,
        "path": request.url.path,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/smart-home-plans")
def add_plan(
    plan: SmartHomeRequest,
    request: Request,
    db: Session = Depends(get_db)
):

    result = create_plan(db, plan)

    return success(
        201,
        "Create success",
        result,
        request
    )

@app.get("/smart-home-plans")
def get_plans(
    request: Request,
    db: Session = Depends(get_db)
):

    result = get_all_plans(db)

    return success(
        200,
        "Get list success",
        result,
        request
    )

@app.get("/smart-home-plans/{plan_id}")
def get_plan(
    plan_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    result = get_plan_by_id(db, plan_id)

    return success(
        200,
        "Get detail success",
        result,
        request
    )
