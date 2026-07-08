from sqlalchemy import Column, Integer, String
from database import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    total_price = Column(Integer, nullable=False)