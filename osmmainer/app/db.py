from config.config import DATABASE_URI
from geoalchemy2 import Geometry
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

engine = create_engine(DATABASE_URI)

metadata = MetaData()
metadata.reflect(bind=engine)

Base = automap_base(metadata=metadata)
Base.prepare()

Marker = Base.classes.markers_marker

session = Session(engine)
