from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import SmartHomePlan

def create_plan(db: Session, plan):

    check = db.query(SmartHomePlan).filter(
        SmartHomePlan.plan_code == plan.plan_code
    ).first()

    if check:
        raise HTTPException(
            status_code=400,
            detail="Plan code already exists"
        )

    try:
        new_plan = SmartHomePlan(
            plan_code=plan.plan_code,
            plan_name=plan.plan_name,
            device_quantity=plan.device_quantity,
            price=plan.price
        )

        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)

        return new_plan

    except:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database Error"
        )

def get_all_plans(db: Session):
    return db.query(SmartHomePlan).all()

def get_plan_by_id(db: Session, plan_id: int):

    plan = db.query(SmartHomePlan).filter(
        SmartHomePlan.id == plan_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    return plan
