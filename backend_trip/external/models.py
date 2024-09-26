from database import Base
from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

metadata = Base.metadata


class User(Base):
    """Mapping to the existing Django user table."""

    __tablename__ = "core_user"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)

    trips = relationship("Trip", back_populates="user")


class Marker(Base):
    """Mapping to the existing Django marker table."""

    __tablename__ = "core_marker"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(Geometry("POINT", srid=4326))

    trips = relationship("Trip", back_populates="marker")
