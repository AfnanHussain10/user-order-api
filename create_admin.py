import sys
import os
from pathlib import Path

# Add parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import UserCreate
from app.services.user import user_service
from app.core.config import settings


def create_admin(db: Session) -> None:
    """
    Create an admin user if no users exist
    """
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "adminpassword")
    
    # Check if admin exists
    admin = user_service.get_by_email(db, admin_email)
    if admin:
        print(f"Admin user {admin_email} already exists")
        return
    
    # Create admin user
    user_in = UserCreate(
        username=admin_username,
        email=admin_email,
        password=admin_password,
        role="admin"
    )
    
    try:
        user = user_service.create(db, user_in)
        print(f"Admin user created with ID: {user.id}")
    except ValueError as e:
        print(f"Error creating admin user: {e}")


def main() -> None:
    """
    Main function to create admin user
    """
    db = SessionLocal()
    try:
        create_admin(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()