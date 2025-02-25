from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base

metadata = Base.metadata


class User(Base):
    """Mapping to the existing Django user table."""

    __tablename__ = "core_user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean)

    trips = relationship("Trip", back_populates="user")
