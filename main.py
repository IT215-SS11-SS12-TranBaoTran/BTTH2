from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from services import get_order_by_id_service
from schemas import OrderResponse

app = FastAPI()

@app.get(
    "/orders/{order_id}", 
    response_model=OrderResponse, 
    status_code=status.HTTP_200_OK
)
def get_order_detail(order_id: int, db: Session = Depends(get_db)):
    order = get_order_by_id_service(db=db, order_id=order_id)
    
    return order