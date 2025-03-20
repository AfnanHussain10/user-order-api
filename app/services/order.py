from typing import List, Optional

from app.repositories.order import order_repository
from app.schemas.order import OrderCreate, OrderUpdate
from app.models.order import Order
from sqlalchemy.orm import Session


class OrderService:
    def get(self, db: Session, order_id: int) -> Optional[Order]:
        return order_repository.get(db=db, id=order_id)
    
    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        return order_repository.get_by_user_id(db=db, user_id=user_id, skip=skip, limit=limit)
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
        return order_repository.get_multi(db=db, skip=skip, limit=limit)
    
    def create(self, db: Session, order_in: OrderCreate, user_id: int) -> Order:
        return order_repository.create_with_user(db=db, obj_in=order_in, user_id=user_id)
    
    def update(self, db: Session, order_id: int, order_in: OrderUpdate) -> Optional[Order]:

        db_obj = self.get(db=db, order_id=order_id)
        if not db_obj:
            return None
        
        return order_repository.update(db=db, db_obj=db_obj, obj_in=order_in)
    
    def delete(self, db: Session, order_id: int) -> Optional[Order]:

        db_obj = self.get(db=db, order_id=order_id)
        if not db_obj:
            return None
        
        return order_repository.remove(db=db, id=order_id)
    
    def is_owner(self, order: Order, user_id: int) -> bool:
        return order.user_id == user_id


order_service = OrderService()