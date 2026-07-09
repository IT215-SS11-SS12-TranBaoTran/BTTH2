from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import models
from database import engine, get_db
from schemas import PlanCreate, PlanResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def format_response(status_code: int, message: str, error: str, data: any, path: str):
    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "message": message,
            "error": error,
            "data": data,
            "path": path,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    )

@app.post("/smart-home-plans")
def create_plan(request: Request, plan_in: PlanCreate, db: Session = Depends(get_db)):
    try:
        existing_plan = db.query(models.SmartHomePlan).filter(models.SmartHomePlan.plan_code == plan_in.plan_code).first()
        if existing_plan:
            return format_response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Plan code already exists",
                error="Bad Request",
                data=None,
                path=str(request.url.path)
            )
        
        new_plan = models.SmartHomePlan(
            plan_code=plan_in.plan_code,
            plan_name=plan_in.plan_name,
            device_quantity=plan_in.device_quantity,
            price=plan_in.price
        )
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)
        
        data_res = PlanResponse.from_orm(new_plan).dict()
        return format_response(
            status_code=status.HTTP_201_CREATED,
            message="Thêm mới gói thiết bị thành công",
            error=None,
            data=data_res,
            path=str(request.url.path)
        )
    except Exception as e:
        db.rollback()
        return format_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Hệ thống gặp sự cố, vui lòng thử lại sau",
            error=str(e),
            data=None,
            path=str(request.url.path)
        )

@app.get("/smart-home-plans")
def get_all_plans(request: Request, db: Session = Depends(get_db)):
    try:
        plans = db.query(models.SmartHomePlan).all()
        data_res = [PlanResponse.from_orm(p).dict() for p in plans]
        return format_response(
            status_code=status.HTTP_200_OK,
            message="Lấy danh sách thành công",
            error=None,
            data=data_res,
            path=str(request.url.path)
        )
    except Exception as e:
        return format_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Hệ thống gặp sự cố",
            error=str(e),
            data=None,
            path=str(request.url.path)
        )

@app.get("/smart-home-plans/{plan_id}")
def get_plan_by_id(plan_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        plan = db.query(models.SmartHomePlan).filter(models.SmartHomePlan.id == plan_id).first()
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        data_res = PlanResponse.from_orm(plan).dict()
        return format_response(
            status_code=status.HTTP_200_OK,
            message="Lấy chi tiết thành công",
            error=None,
            data=data_res,
            path=str(request.url.path)
        )
    except HTTPException as he:
        return format_response(
            status_code=he.status_code,
            message=he.detail,
            error="Not Found",
            data=None,
            path=str(request.url.path)
        )
    except Exception as e:
        return format_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Hệ thống gặp sự cố",
            error=str(e),
            data=None,
            path=str(request.url.path)
        )
