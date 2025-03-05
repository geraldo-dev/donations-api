from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from app.config import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
