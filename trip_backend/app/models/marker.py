from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base

metadata = Base.metadata


class Marker(Base):
    """Mapping to the existing Django marker table."""

    __tablename__ = "core_marker"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(Geometry("POINT", srid=4326))

    trips = relationship("Trip", back_populates="marker")
