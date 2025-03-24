from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.services.order import order_service
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.core.dependencies import get_current_user, get_current_admin

router = APIRouter()


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderResponse:
    """
    Create a new order
    """
    order = order_service.create(db, order_in, current_user.id)
    return order


@router.get("", response_model=List[OrderResponse])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
) -> List[OrderResponse]:
    """
    Retrieve all orders (admin only)
    """
    orders = order_service.get_all(db, skip=skip, limit=limit)
    return orders


@router.get("/me", response_model=List[OrderResponse])
def read_my_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[OrderResponse]:
    """
    Get all orders for the current user
    """
    orders = order_service.get_by_user(db, current_user.id, skip=skip, limit=limit)
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderResponse:
    """
    Get a specific order by ID
    """
    order = order_service.get(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    
    # Check if user is owner or admin
    if not order_service.is_owner(order, current_user.id) and not current_user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    return order


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_in: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderResponse:
    """
    Update an order
    """
    order = order_service.get(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    
    # Check if user is owner or admin
    if not order_service.is_owner(order, current_user.id) and not current_user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    updated_order = order_service.update(db, order_id, order_in)
    return updated_order


@router.delete("/{order_id}", response_model=OrderResponse)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> OrderResponse:
    """
    Delete an order
    """
    order = order_service.get(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    
    # Check if user is owner or admin
    if not order_service.is_owner(order, current_user.id) and not current_user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    order = order_service.delete(db, order_id)
    return order