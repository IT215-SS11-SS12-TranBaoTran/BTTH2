from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import OrderModel

def get_order_by_id_service(db: Session, order_id: int):
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
        
    return order