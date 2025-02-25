from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Trip(Base):
    __tablename__ = "trip_trips"

    id = Column(Integer, primary_key=True, index=True)

    marker_id = Column(Integer, ForeignKey("core_marker.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("core_user.id", ondelete="CASCADE"), nullable=False)

    create_date = Column(Date, default=date.today, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    description = Column(String, nullable=False)

    marker = relationship("Marker", back_populates="trips")
    user = relationship("User", back_populates="trips")
