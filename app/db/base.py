# Import all models here so Alembic can discover them
from app.db.session import Base
from app.models.user import User
from app.models.order import Order

Base.metadata