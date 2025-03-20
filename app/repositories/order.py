from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate


class OrderRepository(BaseRepository[Order, OrderCreate, OrderUpdate]):
    def get_by_user_id(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        # Get all orders for a specific user
        return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

    def create_with_user(self, db: Session, *, obj_in: OrderCreate, user_id: int) -> Order:
        
        obj_in_data = obj_in.model_dump()
        db_obj = Order(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


# Create a repository instance
order_repository = OrderRepository(Order)