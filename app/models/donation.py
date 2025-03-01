from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.config import Base


class Donation(Base):
    __tablename__ = "donations"

    donation_id = Column(Integer, primary_key=True, index=True)
    donor = Column(String, index=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    active = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime, default=func.now())
